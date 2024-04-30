from unittest import TestCase

import os

class CameraTest(TestCase):
    LANGUAGES = {
        'zh': {
            'CameraTest': '摄像头',
            'test_still': '拍照',
        },
        'en': {
            'CameraTest': 'Camera',
            'test_still': 'Still',
        }
    }

    def test_still(self):
        self.assertTrue(os.path.exists('/tmp/cpp0_output_1920x1080_s1920.nv12'))
        self.assertTrue(os.path.exists('/tmp/raw_output0_3840x2160.raw'))
