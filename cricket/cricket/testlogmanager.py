
from PyQt5.QtCore import Qt, QTimer, QObject

class DeviceStatusManager(QObject):
    def __init__(self):
        super().__init__()
        self.time_sync = False
        self.wifi_sync = False
        self.check_mode = 1
        self.set_file_name_flag = False