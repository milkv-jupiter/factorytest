from unittest import TestCase

import subprocess
import threading

from utils.speaker import SpeakerTestWindow, GetTestResult

class HeadphonesTest(TestCase):
    LANGUAGES = {
        'zh': {
            'HeadphonesTest': '耳机',
            'test_play': '播放一段铃声',
            'title': '耳机',
            'test_step': '''1. 插入耳机
2. 点击播放，设备将播放一段铃声，判断从喇叭听到的铃声是否符合预期
'''
        },
        'en': {
            'HeadphonesTest': 'Headphones',
            'test_play': 'Paly bell',
            'title': 'Headphones',
            'test_step': '''1. 插入耳机
2. 点击播放，设备将播放一段铃声，判断从喇叭听到的铃声是否符合预期
'''
        }
    }

    def _play_routine(self):
        volume = 128
        cmd = f'amixer -c 1 cset numid=1,iface=MIXER,name="DAC Playback Volume" {volume}'
        result = subprocess.run(cmd, capture_output=True, shell=True)
        print(f'amixer: {result.returncode}')

        bell_file = '/opt/factorytest/res/nocturne.wav'
        cmd = f'aplay -Dhw:1,0 -r 48000 -f S16_LE {bell_file}'
        self.play_proc = subprocess.Popen(cmd, shell=True)

    def _stop_routine(self):
        if self.play_proc.poll() is None:
            print('Try to kill play process...')
            self.play_proc.kill()

    def test_play(self):
        t = threading.Thread(target=SpeakerTestWindow,
                             args=(self._play_routine,
                                   self._stop_routine,
                                   self.LANGUAGES),)
        t.start()
        t.join()
        self.assertTrue(GetTestResult())