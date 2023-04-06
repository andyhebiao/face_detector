# -*- utf-8 -*-
# @Time:  2022/11/1 13:31
# @Autor: Andy Ye
# @File:  functions.py
# @IDE: PyCharm
import subprocess as sub
from PyQt5.QtWidgets import QFileDialog
import configparser
import time


def load_config(self, info_object=None, file_path=None):
    if not file_path:
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Config File", "./Config", "Config Files(*.cfg)")
    if not file_path:
        return False
    else:
        # print('=====file_path:', file_path)
        cfg = configparser.ConfigParser()
        try:
            cfg.read(file_path, encoding='gbk')
        except UnicodeError:
            cfg.read(file_path, encoding='utf-8')

        for (key, value) in cfg.items("config"):
            if "sb_" + key in dir(self.ui):
                exec("self.ui.sb_" + key + ".setValue(" + value + ")")
                # exec("self." + key + "=" + value)
                print("self." + key + "=" + value)
            elif "ds_" + key in dir(self.ui):
                exec("self.ui.ds_" + key + ".setValue(" + value + ")")
                # exec("self." + key + "=" + value)
                print("self." + key + "=" + value)
            elif "le_" + key in dir(self.ui):
                # print("le_" + key)
                exec("self.ui.le_" + key + ".setText(\"" + value + "\")")
                # exec("self." + key + "=\"" + value + "\"")
                print("self." + key + "=" + value)
            elif key in dir(self):
                exec("self." + key + "=" + value)
                print("self." + key + "=" + value)
            else:
                print("redundant parameters:", key, "=", value)
        if info_object:
            # print("=========info", time.asctime(), file_path)
            info_object.appendPlainText(time.asctime() + "\t" + file_path + " is loaded.")
        return True
