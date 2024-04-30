from unittest import TestCase

import subprocess

class HDMIAudioTest(TestCase):
    LANGUAGES = {
        'zh': {
            'HDMIAudioTest': 'HDMI Audio',
            'test_hdmi_auido': '播放一段音乐'
        },
        'en': {
            'HDMIAudioTest': 'HDMI Audio',
            'test_hdmi_auido': 'Play a piece of music'
        }
    }

    def test_hdmi_auido(self):
        try:
            music_file = '/opt/factorytest/res/canon.wav'
            cmd = f'aplay -Dhw:0,0 -r 48000 -f S16_LE {music_file}'
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
        except:
            self.fail('Create subprocess fail')
