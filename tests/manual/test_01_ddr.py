from unittest import TestCase

import os

class DDRTest(TestCase):
    LANGUAGES = {
        'zh': {
            'DDRTest': '内存',
            'test_capacity': '读取容量'
        },
        'en': {
            'DDRTest': 'DDR',
            'test_capacity': 'Read capacity'
        }
    }

    def test_capacity(self):
        # implement in qtview
        self.assertTrue(os.path.exists('/proc/meminfo'))
