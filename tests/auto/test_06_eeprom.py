from unittest import TestCase

import os

class EEPROMTest(TestCase):
    LANGUAGES = {
        'zh': {
            'EEPROMTest': 'EEPROM',
            'test_read': '读取数据'
        },
        'en': {
            'EEPROMTest': 'EEPROM',
            'test_read': 'Read data'
        }
    }

    def test_read(self):
        eeprom_file = '/sys/devices/platform/soc/d4012000.i2c/i2c-2/2-0050/eeprom'
        self.assertTrue(os.path.exists(eeprom_file))
        try:
            with open(eeprom_file, 'rb') as f:
                f.read(8)
        except:
            self.fail('Read fail')
