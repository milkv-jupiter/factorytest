from unittest import TestCase

import os

class CTPTest(TestCase):
    LANGUAGES = {
        'zh': {
            'CTPTest': '触摸屏',
            'test_read_model': '读取型号'
        },
        'en': {
            'CTPTest': 'CTP',
            'test_read_model': 'Read model'
        }
    }

    def test_read_model(self):
        model_file = '/sys/devices/platform/soc/d4018800.i2c/i2c-6/6-005d/productinfo'
        self.assertTrue(os.path.exists(model_file))