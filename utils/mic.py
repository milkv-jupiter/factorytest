from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFrame,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QStatusBar,
    QPushButton,
    QGridLayout
)

from cricket.lang import SimpleLang

result = False

class MicTestWindow(SimpleLang):
    def __init__(self, record_routine, stop_record, playback_routine, stop_playback, languages) -> None:
        super().__init__()

        self.record_routine = record_routine
        self.stop_record = stop_record
        self.playback_routine = playback_routine
        self.stop_playback = stop_playback
        self.languages = languages

        self.app = QApplication([])

        self.window = QMainWindow()
        self.window.setWindowTitle(self._get_text('title'))
        # self.window.setWindowFlags(Qt.WindowStaysOnTopHint)

        # Main content
        content = QFrame(self.window)
        content_layout = QVBoxLayout(content)

        # Test step
        box = QGroupBox(self.get_text('test_step'), content)
        box_layout = QVBoxLayout(box)

        label = QLabel(self._get_text('test_step'), box)
        box_layout.addWidget(label)

        content_layout.addWidget(box)

        # Status
        self.status = QStatusBar(content)
        self.status.showMessage('Not running')
        content_layout.addWidget(self.status)

        # Toolbar
        toolbar = QFrame(content)
        toolbar_layout = QGridLayout(toolbar)

        self.record_button = QPushButton(self.get_text('record_button'), toolbar)
        self.record_button.clicked.connect(self.cmd_record)
        self.record_button.setFocus()
        toolbar_layout.addWidget(self.record_button, 0, 0)

        self.playback_button = QPushButton(self.get_text('playback_button'), toolbar)
        self.playback_button.setDisabled(True)
        self.playback_button.clicked.connect(self.cmd_playback)
        toolbar_layout.addWidget(self.playback_button, 0, 1)

        self.pass_button = QPushButton(self.get_text('pass_button'), toolbar)
        self.pass_button.setDisabled(True)
        self.pass_button.clicked.connect(self.cmd_pass)
        toolbar_layout.addWidget(self.pass_button, 0, 2)

        self.fail_button = QPushButton(self.get_text('fail_button'), toolbar)
        self.fail_button.setDisabled(True)
        self.fail_button.clicked.connect(self.cmd_fail)
        toolbar_layout.addWidget(self.fail_button, 0, 3)

        content_layout.addWidget(toolbar)

        self.window.setCentralWidget(content)

        # Move to center
        # screen = QGuiApplication.primaryScreen()
        # if screen:
        #     screen_geometry = screen.geometry()
        #     window_geometry = self.window.geometry()
        #     x = (screen_geometry.width() - window_geometry.width()) // 2
        #     y = (screen_geometry.height() - window_geometry.height()) // 2
        #     self.window.move(x, y)

        # self.window.show()
        self.window.showFullScreen()

        self.app.exec_()

    def _get_text(self, key):
        if self.languages:
            lang = self.languages.get(self.current_lang)
            if lang is not None:
                text = lang.get(key)
                if text is not None:
                    return text

        return 'Undefined'

    def cmd_record(self):
        self.status.showMessage('Recording...')
        self.record_button.setDisabled(True)
        self.record_routine()
        self.playback_button.setDisabled(False)

    def cmd_playback(self):
        self.stop_record()

        self.status.showMessage('Playback...')
        self.playback_button.setDisabled(True)
        self.playback_routine()
        self.pass_button.setDisabled(False)
        self.fail_button.setDisabled(False)

    def cmd_pass(self):
        global result

        self.status.showMessage('Stopping...')
        self.stop_playback()
        result = True
        self.app.quit()

    def cmd_fail(self):
        global result

        self.status.showMessage('Stopping...')
        self.stop_playback()
        result = False
        self.app.quit()

def GetTestResult():
    return result