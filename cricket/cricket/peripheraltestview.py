from PyQt5.QtCore import Qt, QTimer, QUrl, QObject, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QPixmap, QImage, QPalette
from PyQt5.QtWidgets import (QWidget, QDialog, QFrame, QHBoxLayout, QVBoxLayout, QLabel,
QPushButton,QLineEdit, QCheckBox,QComboBox, QSizePolicy, QSpacerItem, QTextEdit)

import subprocess
import re
import os
from typing import Tuple, List
from cricket.lang import SimpleLang
from cricket.loggermanager import LoggerManager
from cricket.macro import *
import time


class PeripheralTestWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent
        self.sl = SimpleLang()

        self.info_msg_index = 0

        self.log_manager = LoggerManager(name='PeripheralLogger')
        self.custom_logger = self.log_manager.get_logger()

        self.name_dict = {'EMMC':"EMMC", "SSD":"SSD", 'TF':'TF Card', 'FlashDrive':'U盘'}

        self.th_dict = {'EMMC':50.0*0.25, 'SSD':380*0.25, 'TF':40.0*0.20, 'FlashDrive':50.0*0.25} # key corresponds to name
        self.size_dict = {'EMMC':'1GB'}

        self.test_sequence = []
        self.current_test_index = 0

        self.initUI()
        self.test_sequence.append({"type":"storage", "name": "EMMC",        "control":self.emmc_control,        "output_file":'/dev/mmcblk2',   "seek":0})
        self.test_sequence.append({"type":"storage", "name": "SSD",         "control":self.ssd_control,         "output_file":'/dev/nvme0n1',   "seek":0})
        self.test_sequence.append({"type":"storage", "name": "TF",          "control":self.tf_card_control,     "output_file":'/dev/mmcblk0',   "seek":10240})
        self.test_sequence.append({"type":"storage", "name": "FlashDrive",  "control":self.flash_drive_control, "output_file":'/dev/sda',       "seek":0})

    def initUI(self):
        font_size = 32
        self.setGeometry(200,200, 800, 800)
        self.setStyleSheet(f"font-size: {font_size}px;")
        self.setWindowTitle('Peripheral Test')
        layout = QVBoxLayout()
        self.setLayout(layout)

        # frame, [check_box, commbox, speed_show, result_show]
        # EMMC
        emmc_frame, self.emmc_control = self.gen_storage_device_testing_ui(self.name_dict['EMMC'], font_size=font_size)
        layout.addWidget(emmc_frame)

        # SSD
        ssd_frame, self.ssd_control = self.gen_storage_device_testing_ui(self.name_dict['SSD'], font_size=font_size)
        layout.addWidget(ssd_frame)

        # TF Card
        tf_card_frame, self.tf_card_control = self.gen_storage_device_testing_ui(self.name_dict['TF'], font_size=font_size)
        layout.addWidget(tf_card_frame)

        # U盘
        flash_drive_frame, self.flash_drive_control = self.gen_storage_device_testing_ui(self.name_dict['FlashDrive'], font_size=font_size)
        layout.addWidget(flash_drive_frame)

         # Create a text edit box that displays the run information
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setFixedHeight(100)
        self.text_edit.setStyleSheet("font-size: 18px;")
        layout.addWidget(self.text_edit)

        # call button
        self.test_button = QPushButton('一键测试', self)
        self.test_button.setStyleSheet(f"font-size: {font_size}px;")
        self.test_button.clicked.connect(self.test_all)
        layout.addWidget(self.test_button)


    def gen_storage_device_testing_ui(self, storage_name, font_size=32) -> Tuple[QFrame, List[QWidget]]:
        storage_frame = QFrame(self)
        # storage_frame.setAutoFillBackground(True)
        storage_frame.setPalette(QPalette(QColor('darkgray')))
        storage_layout = QHBoxLayout(storage_frame)

        spacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        storage_layout.addSpacerItem(spacer)

        # check
        check_box_frame = QWidget(storage_frame)
        check_box_layout = QHBoxLayout(check_box_frame)
        storage_check_box = QCheckBox(storage_frame)
        storage_check_box.setStyleSheet("""
            QCheckBox::indicator {
                width: 32px;
                height: 32px;
            }
        """)
        storage_check_box.setChecked(True)
        check_box_layout.addWidget(storage_check_box)

        storage_name_label = QLabel(storage_name, check_box_frame)
        storage_name_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        check_box_layout.addWidget(storage_name_label)

        storage_layout.addWidget(check_box_frame)

        spacer = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        storage_layout.addSpacerItem(spacer)

        # write size
        write_size_frame = QWidget(storage_frame)
        write_size_frame_layout = QHBoxLayout(write_size_frame)
        write_text_label = QLabel('写入大小:', write_size_frame)
        write_text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        write_text_label.setStyleSheet(f"font-size: {font_size}px;")
        write_size_frame_layout.addWidget(write_text_label)

        storage_comm_box = QComboBox(write_size_frame)
        storage_comm_box.addItems(['1GB', '2GB', '3GB', '4GB'])
        storage_comm_box.setStyleSheet(f"font-size: {font_size}px;")
        storage_comm_box.currentText()
        write_size_frame_layout.addWidget(storage_comm_box)
        storage_layout.addWidget(write_size_frame)

        spacer = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        storage_layout.addSpacerItem(spacer)

        # speed result
        speed_frame = QWidget(storage_frame)
        speed_frame_layout = QHBoxLayout(speed_frame)
        speed_text_label = QLabel('速度:', speed_frame)
        speed_text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        speed_text_label.setStyleSheet(f"font-size: {font_size}px;")
        speed_frame_layout.addWidget(speed_text_label)

        storage_speed_show = QLabel('        ', speed_frame)
        storage_speed_show.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        storage_speed_show.setStyleSheet(f"font-size: {font_size}px;")
        speed_frame_layout.addWidget(storage_speed_show)
        storage_layout.addWidget(speed_frame)

        spacer = QSpacerItem(32, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        storage_layout.addSpacerItem(spacer)
        # speed result judgment
        judgment_frame = QWidget(storage_frame)
        judgment_frame_layout = QHBoxLayout(judgment_frame)
        judgment_text_label = QLabel('结果:', judgment_frame)
        judgment_text_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        judgment_text_label.setStyleSheet(f"font-size: {font_size}px;")
        judgment_frame_layout.addWidget(judgment_text_label)

        judgment_show = QLabel('未测', judgment_frame)
        judgment_show.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        judgment_show.setStyleSheet(f"font-size: {font_size}px;")
        judgment_frame_layout.addWidget(judgment_show)
        storage_layout.addWidget(judgment_frame)

        return storage_frame, [storage_check_box, storage_comm_box, storage_speed_show, judgment_show]


    def test_all(self):
        self.test_button.setEnabled(False)
        self.text_edit.append(f"{self.info_msg_index} : 开始测试所有被勾选项目................")
        self.info_msg_index += 1
        self.run_next_test()

    def run_next_test(self):
        if self.current_test_index < len(self.test_sequence):
            test_info = self.test_sequence[self.current_test_index]

            if test_info["type"] == "storage":
                of = test_info["output_file"]
                if test_info["name"] == "FlashDrive":
                    of = self.find_sda_to_sdf_devices()
                self.test_storage_wrapper(test_info["control"], test_info["name"], output_file=of, seek=test_info["seek"])
            elif test_info["type"] == "network":
                pass
        else:
            self.test_button.setEnabled(True)
            self.text_edit.append(f"{self.info_msg_index} : 所有测试项目已完成")
            self.info_msg_index += 1
            self.current_test_index = 0

    # storage function
    def test_storage_wrapper(self, storage_control, test_name, output_file='/dev/mmcblk2', seek=0):
        if storage_control[0].isChecked():
            self.text_edit.append(f"{self.info_msg_index} : 开始测试{self.name_dict[test_name]}写入速度................")
            self.info_msg_index += 1
            size = storage_control[1].currentText()
            size = int(size[0]) * 1024

            self.thread_storage = StorageTestThread(output_file=output_file, size=size, seek=seek)
            self.thread_storage.task_finished.connect(
                lambda msg, storage_control=storage_control, test_name=test_name:self.test_storage_postprocessing(msg, storage_control, test_name))
            self.thread_storage.start()
        else:
            self.current_test_index += 1
            self.run_next_test()

    def test_storage_postprocessing(self, msg, storage_control, test_name):
        ret = msg[0]
        speed = msg[1]
        time_cst = msg[2]
        if type(ret) == str:
            storage_control[2].setText(ret)
        else:
            storage_control[2].setText(f"{speed} MB/S")
            th = self.th_dict[test_name]
            if speed>=th:
                storage_control[3].setText(f"通过")
                storage_control[3].setStyleSheet(f"color: {PASS_COLOR};")
            else:
                storage_control[3].setText(f"失败")
                storage_control[3].setStyleSheet(f"color: {FAIL_COLOR};")
        self.text_edit.append(f"{self.info_msg_index} : {self.name_dict[test_name]}写入速度测试完成, 耗时为{time_cst}s, 返回:{ret}")
        self.info_msg_index += 1

        test_info = self.test_sequence[self.current_test_index]
        if test_info["type"] == "storage":
            self.thread_storage.quit()
            self.thread_storage.wait()
            del self.thread_storage
        elif test_info["type"] == "network":
            pass

         # Move to the next test item
        self.current_test_index += 1
        self.run_next_test()

    def find_sda_to_sdf_devices(self):
        try:
            file_list = ['/dev/'+sub for sub in ['sda', 'sdb', 'sdc', 'sdd', 'sde', 'sdf']]
            for device in file_list:
                if os.path.exists(device):
                    return device
            return '/dev/noexist'
        except Exception as e:
            return '/dev/noexist'

class StorageTestThread(QThread):
    # Defines a signal that notifies the main thread when a thread task has completed
    task_finished = pyqtSignal(list)

    def __init__(self, output_file='', size='', seek=''):
        super().__init__()

        self.output_file = output_file
        self.size = size
        self.seek = seek
        self.speed = None
        self.ret = None

    def run(self):
        t_start = time.time()
        self.ret = self.test_storage_write_speed(output_file=self.output_file, count=self.size, seek=self.seek)
        t_period = time.time() - t_start
        speed = float(self.size)/t_period
        self.speed = round(speed, 1)
        self.task_finished.emit([self.ret, self.speed, round(t_period, 1)])

    def test_storage_write_speed(self, output_file, bs="1M", count=1024, seek=0):
        try:
            if not os.path.exists(output_file):
                return "设备不存在"

            command = ["dd", f"if=/dev/zero", f"of={output_file}", f"bs={bs}", f"count={count}", "oflag=direct", f"seek={seek}"]
            result = subprocess.run(command, stderr=subprocess.PIPE, text=True)
            return 0
        except Exception as e:
            return f"dd命令执行异常{e}"