# -*- utf-8 -*-
# @Time:  2023/4/6 9:07
# @Autor: Andy Ye
# @File:  main.py
# @IDE: PyCharm

from gui_main import *
from functions import load_config
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore
from Webcam.webcam import *
import threading as td
import qimage2ndarray

class FaceDetection(QMainWindow):
    def __init__(self):
        super(FaceDetection, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pb_start.clicked.connect(self.start)
        self.ui.pb_stop.clicked.connect(self.stop)
        load_config(self, info_object=self.ui.pte_info, file_path="./Config/config.cfg")
        self.frame = None
        self.face_detector = None
        self.ui_timer = QtCore.QTimer()
        self.ui_timer.timeout.connect(self.update)
        self.ui_timer.start(30)

    def start(self):
        if self.face_detector is None:
            self.face_detector = FaceDetector(self.ui.sb_camera_index.value(), 1 / self.ui.sb_sampling_rate.value(),
                                         self.ui.sb_face_minimal_size.value(), self.ui.sb_server_port.value(),
                                         self.ui.sb_resolution_width.value(), self.ui.sb_resolution_height.value())
            self.face_detector.start()
            self.ui.pte_info.appendPlainText("Face Detection Started")

    def stop(self):
        if self.face_detector:
            self.face_detector.stop()
            self.face_detector = None
            self.ui.pte_info.appendPlainText("Face Detection Stopped")
    def update(self) -> None:
        lock = td.Lock()
        if self.face_detector:
            with lock:
                rgb_frame = self.face_detector.rgb_frame.copy()
            # print("=====", type(rgb_frame), rgb_frame.shape)
            color = qimage2ndarray.array2qimage(rgb_frame)
            self.ui.ql_frame.setPixmap(
                QPixmap(color).scaled(self.ui.ql_frame.size(), QtCore.Qt.KeepAspectRatio))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FaceDetection()
    window.show()
    sys.exit(app.exec_())