# -*- utf-8 -*-
# @Time:  2022/8/22 15:41
# @Autor: Andy Ye
# @File:  test.py
# @IDE: PyCharm


import cv2
import os
import face_const as fc
import face_detection as fd
import time


def extract_face_pic_haar(frame):
    face = fd.detect_face_haar(frame)
    if len(face) != 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        x, y, w, h = face[0]
        face_img = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
        return face_img
    else:
        return None


def export_pic_face_haar(filenames, export_path=r'D:\faces'):
    n = len(filenames)
    n_len = len(str(n))
    for i in range(n):
        frame = cv2.imread(filenames[i])
        face_img = extract_face_pic_haar(frame)
        cv2.imwrite(export_path + r'\%s%d.pgm' % ("0" * (n_len - len(str(i))), i), face_img)


def export_video_face_haar(source=0, frame_number=20, export_path=r'D:\faces'):
    video = cv2.VideoCapture(source)
    # fps = cv2.VideoCapture.get(cv2.CAP_PROP_FPS)
    # size = (int(cv2.VideoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cv2.VideoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    success, frame = video.read()
    if type(source) == int: time.sleep(0.5)
    i = 0
    while success:
        i += 1
        success, frame = video.read()
        face_img = extract_face_pic_haar(frame)
        cv2.imshow('Capturing Faces...', frame)
        cv2.imwrite(export_path + r'\%d.jpg' % i, face_img)
        if i >= frame_number:
            break



# def export_live_face_haar(frame_number, export_path=r'D:\faces', camera_number=0):
#     video = cv2.VideoCapture(camera_number)
#     success, frame = video.read()
#     i = 0
#     while success:
#         if i >= frame_number:
#             break
#         face_img = extract_face_pic_haar(frame)
#         cv2.imwrite(export_path + r'\%d.pgm' % i, face_img)
#         success, frame = video.read()
#         i += 1


if __name__ == '__main__':
    export_video_face_haar(1)