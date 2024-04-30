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
        # timeout: length * 1.28s
        # devices: numrsp
        scan = 'hcitool -i hci0 scan --length=5 --numrsp=1'
        try:
            proc = subprocess.run(scan, capture_output=True, text=True, shell=True, timeout=10)
            print(proc.stdout)
            self.assertEqual(proc.returncode, 0)
            #self.assertGreater(len(proc.stdout.splitlines()), 1)
        except subprocess.TimeoutExpired:
            self.fail('Scan timeout')
