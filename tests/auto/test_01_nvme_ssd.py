from unittest import TestCase

import os

class NVMeSSDTest(TestCase):
    LANGUAGES = {
        'zh': {
            'NVMeSSDTest': 'NVMe固态硬盘',
            'test_read_model': '读取型号'
        },
        'en': {
            'NVMeSSDTest': 'NVMe SSD',
            'test_read_model': 'Read model'
        }
    }

    def test_read_model(self):
        model_file = '/sys/class/nvme/nvme0/model'
        self.assertTrue(os.path.exists(model_file))