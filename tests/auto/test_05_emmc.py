from unittest import TestCase

import os

class eMMCTest(TestCase):
    LANGUAGES = {
        'zh': {
            'eMMCTest': 'eMMC',
            'test_identify': '识别'
        },
        'en': {
            'eMMCTest': 'eMMC',
            'test_identify': 'Identify'
        }
    }

    def test_identify(self):
        block_file = '/sys/class/block/mmcblk2'
        self.assertTrue(os.path.exists(block_file))