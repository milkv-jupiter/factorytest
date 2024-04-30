from unittest import TestCase

import subprocess
import threading

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

class LCDTestWindow(SimpleLang):
    def __init__(self, languages) -> None:
        super().__init__()

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
        # self.status = QStatusBar(content)
        # self.status.showMessage('Not running')
        # content_layout.addWidget(self.status)

        # Toolbar
        toolbar = QFrame(content)
        toolbar_layout = QGridLayout(toolbar)

        self.pass_button = QPushButton(self.get_text('pass_button'), toolbar)
        # self.pass_button.setDisabled(True)
        self.pass_button.clicked.connect(self.cmd_pass)
        self.pass_button.setFocus()
        toolbar_layout.addWidget(self.pass_button, 0, 0)

        self.fail_button = QPushButton(self.get_text('fail_button'), toolbar)
        # self.fail_button.setDisabled(True)
        self.fail_button.clicked.connect(self.cmd_fail)
        toolbar_layout.addWidget(self.fail_button, 0, 1)

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

    def cmd_pass(self):
        global result

        # self.status.showMessage('Stopping...')
        result = True
        self.app.quit()

    def cmd_fail(self):
        global result

        # self.status.showMessage('Stopping...')
        result = False
        self.app.quit()

class LCDTest(TestCase):
    LANGUAGES = {
        'zh': {
            'LCDTest': 'MIPI屏',
            'test_lcd': '彩色条纹',
            'title': 'MIPI屏',
            'test_step': '''1. 观察MIPI屏彩色条纹是否符合预期
'''
        },
        'en': {
            'LCDTest': 'MIPI Screen',
            'test_lcd': 'Color Bar',
            'title': 'MIPI Screen',
            'test_step': '''1. 观察MIPI屏彩色条纹是否符合预期
'''
        }
    }

    def test_lcd(self):
        global result

        t = threading.Thread(target=LCDTestWindow, args=(self.LANGUAGES,))
        t.start()

        cmd = 'modetest -M spacemit -s 136@127:1200x1920 -a -P 31@127:1200x1920+0+0@AR24'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        t.join()

        if proc.poll() is None:
            print('Try to kill process...')
            proc.kill()

        self.assertTrue(result)
