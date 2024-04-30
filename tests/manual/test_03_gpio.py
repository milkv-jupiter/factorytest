from unittest import TestCase

import subprocess

class GPIOTest(TestCase):
    LANGUAGES = {
        'zh': {
            'GPIOTest': 'GPIO',
            'test_gpio': '开灯'
        },
        'en': {
            'GPIOTest': 'GPIO',
            'test_gpio': 'Turn on light'
        }
    }

    def test_gpio(self):
        try:
            gpios = '47 48 49 50 51 52 70 71 72 73 74 75 76 77 78 90 91 92'
            cmd = f'/opt/factorytest/utils/gpio.sh {gpios}'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        except:
            self.fail('Create gpio subprocess fail')

