# -*- utf-8 -*-
# @Time:  2023/2/17 17:05
# @Autor: Andy Ye
# @File:  osc.py
# @IDE: PyCharm


import threading as td
import argparse
import random
import time
from pythonosc import udp_client


class OscClient(object):
    def __init__(self, server_ip="127.0.0.1", port=9001):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", default=server_ip, help="The ip of the OSC server")
        parser.add_argument("--port", type=int, default=port,  help="The port the OSC server is listening on")
        args = parser.parse_args()
        self.client = udp_client.SimpleUDPClient(args.ip, args.port)

    def send_message(self, *message):
        self.client.send_message(*message)


if __name__ == '__main__':
    osc_client = OscClient("127.0.0.1")
    while True:
        # osc_client.send_message("/data/value", [time.asctime(), 1223])
        # osc_client.send_message("/r/g/b", random.randint(0, 255))
        osc_client.send_message("/r", random.randint(0, 255))
        osc_client.send_message("/g", random.randint(0, 255))
        osc_client.send_message("/b", random.randint(0, 255))
        print(time.asctime())
        time.sleep(1)
