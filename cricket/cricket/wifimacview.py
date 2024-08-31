from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QFrame,QVBoxLayout,QLabel
import subprocess
from cricket.lang import SimpleLang
from cricket.utils import *
import re

class WifiMacView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.sl = SimpleLang()
        self.wifi_mac_text = self.sl.get_text("wifi_mac")

        self.setup_wifi_mac_with_ui()

    def setup_wifi_mac_with_ui(self):
        mac = self._get_wifi_mac()
        if mac:
            self._setup_wifi_mac_qrcode(mac)
        else:
            QTimer.singleShot(2000, self.setup_wifi_mac_with_ui)

    def _get_wifi_mac(self):
        cmd = 'ifconfig wlan0'
        proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=1)

        text = proc.stdout
        pattern = r"HWaddr\s+([0-9A-Fa-f:]{17})"

        match = re.search(pattern, text)
        if match:
            mac_address = match.group(1)
            return mac_address
        else:
            return None

    def _setup_wifi_mac_qrcode(self, mac):
        mac_qrcode_layout = QVBoxLayout(self)

        qr_label = QLabel(self)
        qr_label.setAlignment(Qt.AlignCenter)
        qr_label.setPixmap(create_qrcode(mac))
        mac_qrcode_layout.addWidget(qr_label)

        mac_label = QLabel(f'{self.wifi_mac_text}: {mac}', self)
        mac_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        mac_qrcode_layout.addWidget(mac_label)

        self.mac_layout = mac_qrcode_layout

        # wifi ip
        self.wifi_ip = QLabel(' ', self)
        self.wifi_ip.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.mac_layout.addWidget(self.wifi_ip)