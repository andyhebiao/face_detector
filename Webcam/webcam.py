# -*- utf-8 -*-
# @Time:  2023/2/20 21:05
# @Autor: Andy Ye
# @File:  webcam.py
# @IDE: PyCharm
import time

import cv2
# import argparse
# from pythonosc import udp_client
import threading as td
import numpy as np
from face.face_detection import *
import socket


class FaceDetector(td.Thread):
    def __init__(self, device_index, rgb_sample_time, minial_size, udp_port, width=1280, height=720, daemon=True):
        super().__init__(daemon=daemon)
        self.cap = cv2.VideoCapture(device_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.dt = rgb_sample_time
        self.width = width
        self.height = height
        self.rgb_frame = np.zeros((height, width, 3), dtype="uint8")
        self.minial_size = minial_size
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = ("127.0.0.1", udp_port)
        self.enabled = True

    def run(self):
        lock = td.Lock()
        while self.cap.isOpened() and self.enabled:
            ret, rgb_frame = self.cap.read()
            rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
            faces = detect_face_haar(rgb_frame, minial_size=self.minial_size, classifier="default")
            if faces:
                self.sock.sendto("1".encode("utf-8"), self.addr)
                # print("===faces",  faces)
            else:
                self.sock.sendto("0".encode("utf-8"), self.addr)
            # flip the rgb_frame
            cv2.flip(rgb_frame, 1, rgb_frame)
            with lock:
                self.rgb_frame = rgb_frame.copy()
                # print(self.rgb_frame)
            # if t - t_old > self.dt:  #  send rgb value
            #     # print("t:", t, "t_old", t_old, "dt:", self.dt)
            #     b, g, r = rgb_frame[self.height // 2, self.width // 2]
            #     t_old = t
            #     # self.dt = 0
            #     print("time:", time.asctime(), "b, g, r", b, g, r)
            #     self.osc_client.send_message("/r", int(r))
            #     self.osc_client.send_message("/g", int(g))
            #     self.osc_client.send_message("/b", int(b))
            #     trigger = Trigger(delay=self.delay, duration=self.dt - self.delay,
            #                       callback=self.osc_client.send_message)
            #     trigger.start()
            # cv2.rectangle(rgb_frame, (self.width // 2 - 1, self.height//2 - 1), (self.width // 2 + 1, self.height // 2 + 1),
            #               (0, 255, 0), 1)

            # cv2.imshow('image', rgb_frame)
            #
            # if cv2.waitKey(1) == 27:    # press Esc to exit the loop
            #     break
            time.sleep(self.dt)
        # release cam
        self.cap.release()
        self.sock.close()
        # close window
        cv2.destroyAllWindows()

    def stop(self):
        self.enabled = False
        # self.cap.release()


if __name__ == '__main__':
    camera_index = 1
    sample_time = 0.030
    webcam = FaceDetector(camera_index, sample_time, 40000, 50000, 1280, 720)
    webcam.start()
    webcam.join()
    # trigger = Trigger(delay=2, duration=8, callback=print)
    # trigger.start()
    # while True:
    #     print(time.asctime())
    #     time.sleep(1)