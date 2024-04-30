from unittest import TestCase

import subprocess

class LCDTest(TestCase):
    LANGUAGES = {
        'zh': {
            'LCDTest': 'MIPI屏',
            'test_lcd': '彩色条纹'
        },
        'en': {
            'LCDTest': 'MIPI Screen',
            'test_lcd': 'Color Bar'
        }
    }

    def test_lcd(self):
        try:
            cmd = 'modetest -M spacemit -s 136@127:1200x1920 -a -P 31@127:1200x1920+0+0@AR24'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        except:
            self.fail('Create modetest subprocess fail')
