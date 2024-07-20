from unittest import TestCase

import os

class UDiskTest(TestCase):
    LANGUAGES = {
        'zh': {
            'UDiskTest': 'U盘',
            'test_read_product': '识别产品名称'
        },
        'en': {
            'UDiskTest': 'U Disk',
            'test_read_product': 'Read product name'
        }
    }

    def test_read_product(self):
        u2_hub_dir = '/sys/devices/platform/soc/soc:usb3@0/c0a00000.dwc3/xhci-hcd.0.auto/usb2/2-1/'
        u3_hub_dir = '/sys/devices/platform/soc/soc:usb3@0/c0a00000.dwc3/xhci-hcd.0.auto/usb3/3-1/'
        self.assertTrue(os.path.exists(f'{u2_hub_dir}/product'))
        self.assertTrue(os.path.exists(f'{u3_hub_dir}/product'))
        self.assertTrue(os.path.exists(f'{u2_hub_dir}/2-1.1/product'))
        self.assertTrue(os.path.exists(f'{u2_hub_dir}/2-1.3/product'))
        self.assertTrue(os.path.exists(f'{u3_hub_dir}/3-1.2/product'))
        self.assertTrue(os.path.exists(f'{u3_hub_dir}/3-1.4/product'))
