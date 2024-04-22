from unittest import TestCase

import subprocess

class BTTest(TestCase):
    LANGUAGES = {
        'zh': {
            'BTTest': '蓝牙',
            'test_scan': '扫描'
        },
        'en': {
            'BTTest': 'Bluetooth',
            'test_scan': 'Scan'
        }
    }

    def test_scan(self):
        scan = 'hcitool -i hci0 scan'
        try:
            result = subprocess.run(scan, capture_output=True, shell=True, timeout=10)
            self.assertEqual(result.returncode, 0)
        except subprocess.TimeoutExpired:
            self.fail('Scan timeout')
