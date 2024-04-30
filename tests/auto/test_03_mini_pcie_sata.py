from unittest import TestCase

import os
import subprocess
#import usb.core

class MiniPCIeTest(TestCase):
    LANGUAGES = {
        'zh': {
            'MiniPCIeTest': 'Mini PCIe to SATA',
            'test_read_model': '读取型号'
        },
        'en': {
            'MiniPCIeTest': 'Mini PCIe to SATA',
            'test_read_model': 'Read model'
        }
    }

    def test_read_model(self):
        model_file = '/sys/bus/pci/devices/0002:01:00.0/ata1/host0/target0:0:0/0:0:0:0/model'
        self.assertTrue(os.path.exists(model_file))