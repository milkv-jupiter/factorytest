from unittest import TestCase

import subprocess

class FanTest(TestCase):
    LANGUAGES = {
        'zh': {
            'FanTest': '风扇',
            'test_speed': '开关'
        },
        'en': {
            'FanTest': 'Fan',
            'test_speed': 'On/Off',
            'title': 'Fan'
        }
    }

    def test_speed(self):
        try:
            gpio = 79
            cmd = f'/opt/factorytest/utils/fan.sh {gpio}'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
        except:
            self.fail('Create fan.sh subprocess failed')
