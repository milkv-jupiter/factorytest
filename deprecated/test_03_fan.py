from unittest import TestCase

import threading
import os

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

class FanTestWindow(SimpleLang):
    def __init__(self, speed_routine, languages) -> None:
        super().__init__()

        self.speed_routine = speed_routine
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

        self.speed_button = QPushButton(self.get_text('speed_button'), toolbar)
        self.speed_button.clicked.connect(self.cmd_speed)
        self.speed_button.setFocus()
        toolbar_layout.addWidget(self.speed_button, 0, 0)

        self.pass_button = QPushButton(self.get_text('pass_button'), toolbar)
        self.pass_button.setDisabled(True)
        self.pass_button.clicked.connect(self.cmd_pass)
        toolbar_layout.addWidget(self.pass_button, 0, 1)

        self.fail_button = QPushButton(self.get_text('fail_button'), toolbar)
        self.fail_button.setDisabled(True)
        self.fail_button.clicked.connect(self.cmd_fail)
        toolbar_layout.addWidget(self.fail_button, 0, 2)

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

    def cmd_speed(self):
        self.speed_routine()
        self.pass_button.setDisabled(False)
        self.fail_button.setDisabled(False)

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

class FanTest(TestCase):
    LANGUAGES = {
        'zh': {
            'FanTest': '风扇',
            'test_speed': '变速',
            'title': '风扇',
            'test_step': '''1. 检查风扇是否正常转动
2. 点击变速，检查风扇转速是否随之变化
'''
        },
        'en': {
            'FanTest': 'Fan',
            'test_speed': 'Speed',
            'title': 'Fan',
            'test_step': '''1. 检查风扇是否正常转动
2. 点击变速，检查风扇转速是否随之变化
'''
        }
    }

    def _speed_routine(self):
        pass

    def test_speed(self):
        global result

        t = threading.Thread(target=FanTestWindow, args=(self._speed_routine,
                                                         self.LANGUAGES,))
        t.start()
        t.join()

        self.assertTrue(result)
