from unittest import TestCase

import os
import subprocess
#import usb.core

class USB4GModuleTest(TestCase):
    LANGUAGES = {
        'zh': {
            'USB4GModuleTest': '4G模块',
            'test_read_product': '读取型号'
        },
        'en': {
            'USB4GModuleTest': '4G Moduel',
            'test_read_product': 'Read product name'
        }
    }

    def test_read_product(self):
        product_file = '/sys/devices/platform/soc/c0980100.ehci1/usb1/1-1/product'
        self.assertTrue(os.path.exists(product_file))

        try:
            timeout = 10
            cmd = 'mmcli -m 0'
            proc = subprocess.run(cmd, shell=True, capture_output=True,
                                  text=True, timeout=timeout)
            print(f'Create mmcli subprocess return {proc.returncode}')
            self.assertEqual(proc.returncode, 0)
            if 'sim-missing' in proc.stdout:
                self.fail('sim-card missing')
        except:
            self.fail('Create mmcli subprocess failed')