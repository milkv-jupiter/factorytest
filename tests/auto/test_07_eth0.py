from unittest import TestCase

import os
import time
import socket
import struct
import fcntl
import subprocess

class Eth0Test(TestCase):
    LANGUAGES = {
        'zh': {
            'Eth0Test': '网口1',
            'test_ping': 'ping'
        },
        'en': {
            'Eth0Test': '网口1',
            'test_ping': 'ping'
        }
    }

    def get_carrier(self, ifname: str):
        carrier = f'/sys/class/net/{ifname}/carrier'

        with open(carrier, 'r') as f:
            return f.readline().strip()

    def get_ip(self, ifname: str):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', bytes(ifname[:15],'utf-8'))
            )[20:24])

    def test_ping(self):
        ifname = 'eth0'
        ping = f'ping -I {ifname} -c 3 baidu.com'
        timeout = 10

        i = 0
        while i < timeout:
            if self.get_carrier(ifname) == '1':
                break

            time.sleep(1)
            i += 1

        if i == timeout:
            self.fail('Get carrier imeout')

        i = 0
        while i < timeout:
            try:
                ip = self.get_ip(ifname)
                print(f'{ifname}: {ip}')
                break
            except:
                time.sleep(1)
                i += 1

        if i == timeout:
            self.fail('Get ip timeout')

        try:
            result = subprocess.run(ping, capture_output=True, shell=True, timeout=timeout)
            self.assertEqual(result.returncode, 0)
        except subprocess.TimeoutExpired:
            self.fail('Ping timeout')
