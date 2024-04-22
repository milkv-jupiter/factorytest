"""A module containing a visual representation of the testModule.

This is the "View" of the MVC world.
"""

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QMainWindow,
    QFrame,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QGroupBox,
    QTableWidget,
    QStatusBar,
    QTableWidgetItem
)

import os
from importlib import import_module

from cricket.model import TestMethod, TestCase, TestModule
from cricket.executor import Executor
from cricket.lang import SimpleLang


# Display constants for test status
STATUS = {
    TestMethod.STATUS_PASS: {
        'description': u'Pass',
        'symbol': u'\u25cf',
        'tag': 'pass',
        'color': '#28C025',
    },
    TestMethod.STATUS_SKIP: {
        'description': u'Skipped',
        'symbol': u'S',
        'tag': 'skip',
        'color': '#259EBF'
    },
    TestMethod.STATUS_FAIL: {
        'description': u'Failure',
        'symbol': u'F',
        'tag': 'fail',
        'color': '#E32C2E'
    },
    TestMethod.STATUS_EXPECTED_FAIL: {
        'description': u'Expected\n  failure',
        'symbol': u'X',
        'tag': 'expected',
        'color': '#3C25BF'
    },
    TestMethod.STATUS_UNEXPECTED_SUCCESS: {
        'description': u'Unexpected\n   success',
        'symbol': u'U',
        'tag': 'unexpected',
        'color': '#C82788'
    },
    TestMethod.STATUS_ERROR: {
        'description': 'Error',
        'symbol': u'E',
        'tag': 'error',
        'color': '#E4742C'
    },
}

STATUS_DEFAULT = {
    'description': 'Not\nexecuted',
    'symbol': u'',
    'tag': None,
    'color': '#BFBFBF',
}


class MainWindow(QMainWindow, SimpleLang):
    def __init__(self, root):
        super().__init__()

        self._project = None
        self.test_table = {}
        self.test_list = {}
        self.run_status = {}
        self.executor = {}

        self.root = root
        self.setWindowTitle(self.get_text('title'))
        # self.showFullScreen()

        # Set up the main content for the window.
        self._setup_main_content()

        # Set up listeners for runner events.
        Executor.bind('test_status_update', self.on_executorStatusUpdate)
        Executor.bind('test_start', self.on_executorTestStart)
        Executor.bind('test_end', self.on_executorTestEnd)
        Executor.bind('suite_end', self.on_executorSuiteEnd)
        Executor.bind('suite_error', self.on_executorSuiteError)

    ######################################################
    # Internal GUI layout methods.
    ######################################################
        
    def _setup_main_content(self):
        '''
        The button toolbar runs as a horizontal area at the top of the GUI.
        It is a persistent GUI component
        '''

        self.content = QFrame(self)
        self.content_layout = QVBoxLayout(self.content)

        toolbar = QFrame(self.content)
        layout = QGridLayout(toolbar)

        self.run_all_button = QPushButton(self.get_text('run_all_button'), toolbar)
        self.run_all_button.clicked.connect(self.cmd_run_all)
        self.run_all_button.setFocus()
        layout.addWidget(self.run_all_button, 0, 0)

        self.run_selected_button = QPushButton(self.get_text('run_selected_button'),
                                               toolbar)
        self.run_selected_button.setDisabled(True)
        self.run_selected_button.clicked.connect(self.cmd_run_selected)
        layout.addWidget(self.run_selected_button, 0, 1)

        self.stop_button = QPushButton(self.get_text('stop_button'), toolbar)
        self.stop_button.setDisabled(True)
        self.stop_button.clicked.connect(self.cmd_stop)
        layout.addWidget(self.stop_button, 0 , 2)

        self.reboot_button = QPushButton(self.get_text('reboot_button'), toolbar)
        self.reboot_button.clicked.connect(self.cmd_reboot)
        layout.addWidget(self.reboot_button, 0, 3)

        self.poweroff_button = QPushButton(self.get_text('poweroff_button'), toolbar)
        self.poweroff_button.clicked.connect(self.cmd_poweroff)
        layout.addWidget(self.poweroff_button, 0, 4)
    
        self.content_layout.addWidget(toolbar)

        self.setCentralWidget(self.content)

    def _setup_test_table(self, name):
        module = import_module(name)

        box = QGroupBox(module.MODULE_NAME[self.current_lang], self.content)
        layout = QVBoxLayout(box)

        columns = self.get_text('test_table_head')

        table = QTableWidget(box)
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.itemSelectionChanged.connect(self.on_testMethodSelected)
        layout.addWidget(table)
        self.test_table[name] = table

        status = QStatusBar(box)
        status.showMessage('Not running')
        layout.addWidget(status)
        self.run_status[name] = status

        self.content_layout.addWidget(box)

    ######################################################
    # Handlers for setting a new project
    ######################################################

    @property
    def project(self):
        return self._project

    def _get_text(self, subModuleName, subModule, key):
        module = import_module(subModule.parent.path)
        testcase = getattr(module, subModuleName)
        if hasattr(testcase, 'LANGUAGES'):
            langs = getattr(testcase, 'LANGUAGES')
            lang = langs.get(self.current_lang)
            if lang is not None:
                text = lang.get(key)
                if text is not None:
                    return text

        return key

    def _add_test_module(self, parentNode, testModule):
        for subModuleName, subModule in sorted(testModule.items()):
            if isinstance(subModule, TestModule):
                self._add_test_module(parentNode, subModule)
            else:
                for testMethod_name, testMethod in sorted(subModule.items()):
                    self.test_list.setdefault(parentNode, []).append(testMethod.path)

                    table = self.test_table[parentNode]
                    row = table.rowCount()
                    table.insertRow(row)
                    item = QTableWidgetItem(self._get_text(subModuleName, subModule, subModuleName))
                    table.setItem(row, 0, item)
                    item = QTableWidgetItem(self._get_text(subModuleName, subModule, testMethod_name))
                    table.setItem(row, 1, item)
                    item = QTableWidgetItem('')
                    item.setData(Qt.UserRole, testMethod.path)
                    table.setItem(row, 2, item)

    @project.setter
    def project(self, project):
        self._project = project

        # Get a count of active tests to display in the status bar.
        # count, labels = self.project.find_tests(True)
        # self.run_summary.set('T:%s P:0 F:0 E:0 X:0 U:0 S:0' % count)

        # Populate the initial tree nodes. This is recursive, because
        # the tree could be of arbitrary depth.
        for testModule_name, testModule in sorted(project.items()):
            self._setup_test_table(testModule_name)
            self._add_test_module(testModule_name, testModule)
            self.executor[testModule_name] = None

        self.showFullScreen()

        TestMethod.bind('status_update', self.on_nodeStatusUpdate)

    ######################################################
    # TK Main loop
    ######################################################

    def mainloop(self):
        self.root.exec_()

    ######################################################
    # User commands
    ######################################################
        
    def cmd_poweroff(self):
        self.stop()
        # self.root.quit()
        os.system('poweroff')

    def cmd_reboot(self):
        self.stop()
        # self.root.quit()
        os.system('reboot')

    def cmd_quit(self):
        "Command: Quit"
        # If the runner is currently running, kill it.
        self.stop()

        self.root.quit()

    def cmd_stop(self, event=None):
        "Command: The stop button has been pressed"
        self.stop()

    def cmd_run_all(self, event=None):
        "Command: The Run all button has been pressed"
        # If the executor isn't currently running, we can
        # start a test run.
        for module, executor in self.executor.items():
            if not executor or not executor.is_running:
                self.run(module)

    def cmd_run_selected(self, event=None):
        "Command: The 'run selected' button has been pressed"
        for module, table in self.test_table.items():
            # If the executor isn't currently running, we can
            # start a test run.
            labels = []
            for item in table.selectedItems():
                data = item.data(Qt.UserRole)
                if data is not None:
                    labels.append(data)

            if labels and (not self.executor[module] or 
                           not self.executor[module].is_running):
                self.run(module, labels=labels)

    ######################################################
    # GUI Callbacks
    ######################################################

    def on_testMethodSelected(self):
        "Event handler: a test case has been selected in the tree"
        # update "run selected" button enabled state
        self.set_selected_button_state()

    def on_nodeStatusUpdate(self, node):
        "Event handler: a node on the tree has received a status update"
        module = node.path.split('.')[0]
        table = self.test_table[module]
        columnCount = table.columnCount()
        for row in range(table.rowCount()):
            item = table.item(row, columnCount-1)
            if item is not None:
                if item.data(Qt.UserRole) == node.path:
                    for column in range(columnCount):
                        _item = table.item(row, column)
                        _item.setForeground(QColor(STATUS[node.status]['color']))
                    item.setText(STATUS[node.status]['description'])
                    break

    def on_testProgress(self, executor):
        "Event handler: a periodic update to poll the runner for output, generating GUI updates"
        if executor and executor.poll():
            QTimer.singleShot(100, lambda: self.on_testProgress(executor))

    def on_executorStatusUpdate(self, event, module, update):
        "The executor has some progress to report"
        # Update the status line.
        self.run_status[module].showMessage(update)

    def on_executorTestStart(self, event, module, test_path):
        "The executor has started running a new test."
        # Update status line
        self.run_status[module].showMessage('Running %s...' % test_path)

    def on_executorTestEnd(self, event, module, test_path, result, remaining_time):
        "The executor has finished running a test."
        self.run_status[module].showMessage('')
        # Update the progress meter
        # self.progress_value.set(self.progress_value.get() + 1)

        # Update the run summary
        # self.run_summary.set('T:%(total)s P:%(pass)s F:%(fail)s E:%(error)s X:%(expected)s U:%(unexpected)s S:%(skip)s, ~%(remaining)s remaining' % {
        #     'total': self.executor.total_count,
        #     'pass': self.executor.result_count.get(TestMethod.STATUS_PASS, 0),
        #     'fail': self.executor.result_count.get(TestMethod.STATUS_FAIL, 0),
        #     'error': self.executor.result_count.get(TestMethod.STATUS_ERROR, 0),
        #     'expected': self.executor.result_count.get(TestMethod.STATUS_EXPECTED_FAIL, 0),
        #     'unexpected': self.executor.result_count.get(TestMethod.STATUS_UNEXPECTED_SUCCESS, 0),
        #     'skip': self.executor.result_count.get(TestMethod.STATUS_SKIP, 0),
        #     'remaining': remaining_time
        # })

        # If the test that just fininshed is the one (and only one)
        # selected on the tree, update the display.
        # current_tree = self.current_test_tree
        # if len(current_tree.selection()) == 1:
        #     # One test selected.
        #     if current_tree.selection()[0] == test_path:
        #         # If the test that just finished running is the selected
        #         # test, force reset the selection, which will generate a
        #         # selection event, forcing a refresh of the result page.
        #         current_tree.selection_set(current_tree.selection())
        # else:
        #     # No or Multiple tests selected
        #     self.name.set('')
        #     self.test_status.set('')

        #     self.duration.set('')
        #     self.description.delete('1.0', END)

        #     self._hide_test_output()
        #     self._hide_test_errors()

    def on_executorSuiteEnd(self, event, module, error=None):
        "The test suite finished running."
        # Display the final results
        self.run_status[module].showMessage('Finished.')

        # if error:
        #     TestErrorsDialog(self.root, error)

        # if self.executor[module].any_failed:
        #     dialog = tkMessageBox.showerror
        # else:
        #     dialog = tkMessageBox.showinfo

        # message = ', '.join(
        #     '%d %s' % (count, TestMethod.STATUS_LABELS[state])
        #     for state, count in sorted(self.executor[module].result_count.items()))

        # dialog(message=message or 'No tests were ran')

        # Reset the running summary.
        # self.run_summary.set('T:%(total)s P:%(pass)s F:%(fail)s E:%(error)s X:%(expected)s U:%(unexpected)s S:%(skip)s' % {
        #     'total': self.executor.total_count,
        #     'pass': self.executor.result_count.get(TestMethod.STATUS_PASS, 0),
        #     'fail': self.executor.result_count.get(TestMethod.STATUS_FAIL, 0),
        #     'error': self.executor.result_count.get(TestMethod.STATUS_ERROR, 0),
        #     'expected': self.executor.result_count.get(TestMethod.STATUS_EXPECTED_FAIL, 0),
        #     'unexpected': self.executor.result_count.get(TestMethod.STATUS_UNEXPECTED_SUCCESS, 0),
        #     'skip': self.executor.result_count.get(TestMethod.STATUS_SKIP, 0),
        # })

        # Reset the buttons
        self.reset_button_states_on_end()

        # Drop the reference to the executor
        self.executor[module] = None

    def on_executorSuiteError(self, event, module, error):
        "An error occurred running the test suite."
        # Display the error in a dialog
        self.run_status[module].showMessage('Error running test suite.')
        # FailedTestDialog(self.root, error)

        # Drop the reference to the executor
        self.executor[module] = None

    def reset_button_states_on_end(self):
        "A test run has ended and we should enable or disable buttons as appropriate."
        is_stoped = True
        for executor in self.executor.values():
            if executor and executor.is_running:
                is_stoped = False

        if is_stoped:
            self.stop_button.setDisabled(True)
            self.run_all_button.setDisabled(False)

        self.set_selected_button_state()

    def set_selected_button_state(self):
        is_running = False
        for executor in self.executor.values():
            if executor and executor.is_running:
                is_running = True

        is_selected = False
        for table in self.test_table.values():
            if table.selectedItems():
                is_selected = True

        if is_running:
            self.run_selected_button.setDisabled(True)
        elif is_selected:
            self.run_selected_button.setDisabled(False)
        else:
            self.run_selected_button.setDisabled(True)

    ######################################################
    # GUI utility methods
    ######################################################

    def run(self, module, active=True, status=None, labels=None):
        """Run the test suite.

        If active=True, only active tests will be run.
        If status is provided, only tests whose most recent run
            status matches the set provided will be executed.
        If labels is provided, only tests with those labels will
            be executed
        """
        labels = labels if labels else self.test_list[module]

        self.run_status[module].showMessage('Running...')
        # self.run_summary.set('T:%s P:0 F:0 E:0 X:0 U:0 S:0' % count)

        self.run_all_button.setDisabled(True)
        self.run_selected_button.setDisabled(True)
        self.stop_button.setDisabled(False)

        # self.progress['maximum'] = count
        # self.progress_value.set(0)

        # Create the runner
        self.executor[module] = Executor(self.project, module, len(labels), labels)

        # Queue the first progress handling event
        QTimer.singleShot(100, lambda: self.on_testProgress(self.executor[module]))

    def stop(self):
        "Stop the test suite."
        for module, executor in self.executor.items():
            if executor and executor.is_running:
                self.run_status[module].showMessage('Stopping...')

                executor.terminate()
                executor = None

                self.run_status[module].showMessage('Stopped.')

        self.reset_button_states_on_end()

    def _hide_test_output(self):
        "Hide the test output panel on the test results page"
        self.output_label.grid_remove()
        self.output.grid_remove()
        self.output_scrollbar.grid_remove()
        self.details_frame.rowconfigure(3, weight=0)

    def _show_test_output(self, content):
        "Show the test output panel on the test results page"
        self.output.delete('1.0', END)
        self.output.insert('1.0', content)

        self.output_label.grid()
        self.output.grid()
        self.output_scrollbar.grid()
        self.details_frame.rowconfigure(3, weight=5)

    def _hide_test_errors(self):
        "Hide the test error panel on the test results page"
        self.error_label.grid_remove()
        self.error.grid_remove()
        self.error_scrollbar.grid_remove()

    def _show_test_errors(self, content):
        "Show the test error panel on the test results page"
        self.error.delete('1.0', END)
        self.error.insert('1.0', content)

        self.error_label.grid()
        self.error.grid()
        self.error_scrollbar.grid()