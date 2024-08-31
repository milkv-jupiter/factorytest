from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QKeyEvent, QMouseEvent, QPixmap, QImage, QPalette
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QGridLayout, QLabel, QProgressBar, QSlider
import subprocess
from cricket.lang import SimpleLang
from cricket.loggermanager import LoggerManager
from cricket.macro import *
from cricket.utils import *

class StatusView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self._setup_others_status()

    def _setup_others_status(self):
        self.others_status_layout = QHBoxLayout(self)

        # wifi signal
        self.wifi_signal_view = WifiSignalView(self)
        self.others_status_layout.addWidget(self.wifi_signal_view)
        self.wifi_signal_view.start_to_scan()


class WifiSignalView(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.sl = SimpleLang()
        self.log_manager = LoggerManager(name='WiFiSignalView')
        self.logger = self.log_manager.get_logger()

        self.wifi_text = self.sl.get_text("wifi")
        self.wifi_ready = False

        self.setup_wifi_signal_with_ui()

    def setup_wifi_signal_with_ui(self):
        wifi_layout = QGridLayout(self)

        wifi_label = QLabel(f'{self.wifi_text}: ', self)
        wifi_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        wifi_layout.addWidget(wifi_label, 0, 0)

        self.wifi_signal_level = QProgressBar(self)
        self.wifi_signal_level.setAlignment(Qt.AlignLeft)
        self.wifi_signal_level.setMaximum(100)

        wifi_layout.addWidget(self.wifi_signal_level, 0, 1)

        self.logger.info(f'{self.sl.get_text("wifi_signal_init")}')
        self.wifi_signal_level.setFormat(f'{self.sl.get_text("wifi_signal_init")}')
        self.wifi_signal_level.setValue(0)

    def start_to_scan(self):
        self.on_wifiStatusUpdate()

    def on_wifiStatusUpdate(self):
        interface = 'wlan0'
        status = self.check_interface_status(interface)
        wifi_module_name = '8852bs'
        kernel_module_wifi_status = self.check_module_loaded(wifi_module_name)
        wpa_supplicant_status = self.check_process_running('wpa_supplicant')
        if status and kernel_module_wifi_status and wpa_supplicant_status:
            self.wifi_ready = True
            pr = f"Interface {interface} is {status}"
            self.set_wifi_signal_level()
        else:
            pr = f"fail wifi: {interface}:{status}, {wifi_module_name}:{kernel_module_wifi_status}, wpa_supplicant:{wpa_supplicant_status}"
            self.logger.info(pr)
            self.wifi_signal_level.setFormat(f'{self.sl.get_text("wifi_signal_init")}')
            self.wifi_signal_level.setValue(0)

        QTimer.singleShot(1000, lambda: self.on_wifiStatusUpdate())

    def check_interface_status(self, interface):
        try:
            # Execute a command ip link show interface
            result = subprocess.run(['ip', 'link', 'show', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # Check the return code of the command execution
            if result.returncode != 0:
                print(f"Error: {result.stderr}")
                return None

            # Analytic output
            output = result.stdout
            if interface in output:
                return True
            else:
                return False
        except Exception as e:
            print(f"Exception occurred: {e}")
            return False

    def check_module_loaded(self, module_name):
        """Check whether the kernel module is loaded successfully"""
        result = subprocess.run(['lsmod'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if module_name in result.stdout:
            return True
        return False

    def check_process_running(self, process_name):
        """Check whether the process is running"""
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if process_name in result.stdout:
            return True
        return False

    def set_wifi_signal_level(self):
        ssid, signal_level = self._get_strongest_wifi()
        if not ssid:
            self.wifi_signal_level.setFormat(f'{self.sl.get_text("wifi_signal_init")}')
            # self.wifi_signal_level.setStyleSheet('QProgressBar { text-align: center; } QProgressBar::chunk { background-color: %s; }' % FAIL_COLOR)
            self.wifi_signal_level.setValue(0)
            return

        if signal_level <= -100:
            self.wifi_signal_level.setStyleSheet('QProgressBar { text-align: center; } QProgressBar::chunk { background-color: %s; }' % FAIL_COLOR)
            value = 20
        elif signal_level <= -88: # (-100, -88]
            self.wifi_signal_level.setStyleSheet('QProgressBar { text-align: center; } QProgressBar::chunk { background-color: %s; }' % FAIL_COLOR)
            value = 40
        elif signal_level <= -55: # (-88, -55]
            self.wifi_signal_level.setStyleSheet('QProgressBar { text-align: center; } QProgressBar::chunk { background-color: %s; }' % FAIL_COLOR)
            value = 60
        elif signal_level <= -33: # (-33, -55]
            self.wifi_signal_level.setStyleSheet('QProgressBar { text-align: center; } QProgressBar::chunk { background-color: %s; }' % PASS_COLOR)
            value = 80
        else: # > -33
            self.wifi_signal_level.setStyleSheet('QProgressBar { text-align: center; } QProgressBar::chunk { background-color: %s; }' % PASS_COLOR)
            value = 100


        # The value is a string encoded in UTF-8
        byte_str = bytes(ssid, 'latin1').decode('unicode_escape').encode('latin1')
        decoded_str = byte_str.decode('utf-8')
        self.wifi_signal_level.setFormat(f'{decoded_str}: {signal_level}')
        self.wifi_signal_level.setValue(value)

    def _get_strongest_wifi(self):
        strongest_signal_level = -2147483648
        strongest_ssid = None

        timeout = 5
        cmd = 'wpa_cli scan'
        scan = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=timeout)
        # if scan.returncode != 0:
        #     return strongest_ssid, strongest_signal_level

        cmd = 'wpa_cli scan_results'
        proc = subprocess.run(cmd, capture_output=True, text=True, shell=True, timeout=timeout)
        if proc.returncode != 0:
            return strongest_ssid, strongest_signal_level

        for line in proc.stdout.splitlines():
            if not line.strip() or line.startswith('Selected interface') or line.startswith('bssid'):
                continue

            parts = line.split('\t')
            if len(parts) < 5:
                continue

            signal_level = int(parts[2])
            ssid = parts[4]

            if signal_level > strongest_signal_level:
                strongest_signal_level = signal_level
                strongest_ssid = ssid

        return strongest_ssid, strongest_signal_level

