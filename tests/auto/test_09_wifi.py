from unittest import TestCase

import subprocess
import time

class WiFiTest(TestCase):
    LANGUAGES = {
        'zh': {
            'WiFiTest': 'WiFi',
            'test_scan': '扫描'
        },
        'en': {
            'WiFiTest': 'WiFi',
            'test_scan': 'Scan'
        }
    }

    def _wpa_cli(self, command):
        timeout = 10
        cmd = f'wpa_cli -p/var/run/wpa_supplicant -iwlan0 {command}'
        proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=timeout)
        print(f'Create wpa_cli subprocess run {command} return {proc.returncode}')
        return proc.returncode, proc.stdout

    def test_scan(self):
        try:
            timeout = 10
            cmd = 'pidof wpa_supplicant'
            proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=timeout)
            if proc.returncode:
                cmd = 'wpa_supplicant -B -Dnl80211 -iwlan0 -c/etc/wpa_supplicant.conf'
                proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=timeout)
                print(f'Create wpa_supplicant subprocess return {proc.returncode}')
                self.assertEqual(proc.returncode, 0)

            rc, out = self._wpa_cli('scan')
            print(out)
            self.assertEqual(rc, 0)

            i = 0
            while i < timeout:
                rc, out = self._wpa_cli('scan_results')
                print(out)
                self.assertEqual(rc, 0)
                if len(out.splitlines()) > 1:
                    break
                time.sleep(1)
                i += 1

            if i == timeout:
                self.fail('scan results without ap')
        except subprocess.TimeoutExpired:
            self.fail('Scan failed')
