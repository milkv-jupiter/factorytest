from unittest import TestCase

import subprocess
import threading

from utils.mic import MicTestWindow, GetTestResult

class MicrophoneTest(TestCase):
    LANGUAGES = {
        'zh': {
            'MicrophoneTest': '耳麦',
            'test_mic_loop': '录音回放',
            'title': '耳麦',
            'test_step': '''1. 插入耳机
2. 点击录音，对着耳麦说：测试1、2、3、4、5
3. 点击停止，判断从喇叭听到的是否刚才对着开发板说的
'''
        },
        'en': {
            'MicrophoneTest': 'Microphone',
            'test_mic_loop': 'Record and playback',
            'title': 'Microphone',
            'test_step': '''1. 插入耳机
2. 点击录音，对着耳麦说：测试1、2、3、4、5
3. 点击停止，判断从喇叭听到的是否刚才对着开发板说的
'''
        }
    }

    def _record_routine(self):
        volume = 191
        cmd = f'amixer -c 1 cset numid=7,iface=MIXER,name="ADC Capture Volume" {volume},{volume}'
        result = subprocess.run(cmd, capture_output=True, shell=True)
        print(f'capture amixer: {result.returncode}')

        timeout = 10
        record_file = '/tmp/record.wav'
        cmd = f'arecord -Dhw:1,0 -r 48000 -f S16_LE -d {timeout} {record_file}'
        self.record_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

    def _stop_record(self):
        if self.record_proc.poll() is None:
            print('Try to kill record process...')
            self.record_proc.kill()

    def _playback_routine(self):
        volume = 160
        cmd = f'amixer -c 1 cset numid=1,iface=MIXER,name="DAC Playback Volume" {volume}'
        result = subprocess.run(cmd, capture_output=True, shell=True)
        print(f'playback amixer: {result.returncode}')

        cmd = 'aplay -Dhw:1,0 -r 48000 -f S16_LE /tmp/record.wav'
        self.playback_proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)

    def _stop_playback(self):
        if self.playback_proc.poll() is None:
            print('Try to kill playback process...')
            self.playback_proc.kill()

    def test_mic_loop(self):
        t = threading.Thread(target=MicTestWindow,
                             args=(self._record_routine,
                                   self._stop_record,
                                   self._playback_routine,
                                   self._stop_playback,
                                   self.LANGUAGES),)
        t.start()
        t.join()
        self.assertTrue(GetTestResult())