#!/usr/bin/env python

import os
import cv2
from threading import Thread
from app import ComputerVisionApp
from argparse import ArgumentParser
from datetime import datetime
from time import sleep


# Definition of output format
WIDTH, HEIGHT = 80, 60
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.join(HERE, 'data')
DEFAULT_FMT = 'ppm'


def now_str():
    return str(datetime.now()).replace(':','').replace(' ','_')


class CaptureThread(Thread):
    running = False
    callback = None
    exit = False

    def run(self):
        while not self.exit:
            if self.running:
                self.callback()
                sleep(1)

    def toggle(self):
        self.running = not self.running
        print "Capture", "started" if self.running else "stopped"


class App(ComputerVisionApp):
    def __init__(self, folder=DEFAULT_ROOT, gray=True, format=DEFAULT_FMT, size=None):
        self.folder = folder
        self.channels = 1 if gray else 3
        self.ext = format
        self.size = size
        folder = os.path.join(folder, now_str()) if folder == DEFAULT_ROOT else folder
        if not os.path.isdir(folder):
            os.makedirs(folder)
            print "Created:", folder
        self.folder = folder
        self.thread = CaptureThread()
        self.thread.callback = self.save_frame
        self.thread.start()

    def on_space(self):
        self.save_frame()

    def do_b(self):
        self.thread.toggle()

    def save_frame(self):
        frame = self.get_frame()
        now = now_str()
        filename = now + '.' + self.ext
        outpath = os.path.join(self.folder, filename)
        if self.size is not None:
            frame = cv2.resize(frame, self.size)
        cv2.imwrite(outpath, frame)
        print now, '- Captured frame: ', outpath

    def on_escape(self):
        self.thread.exit = True
        raise SystemExit("Clean exit")


if __name__ == "__main__":
    parser = ArgumentParser(description="Open a capture device and save frames to a folder")
    parser.add_argument('-o', '--output', default=DEFAULT_ROOT, type=str, help="Path to destination folder (must be writable)")
    parser.add_argument('-W', '--width', default=WIDTH, type=int, help="Captured image width (pixels)")
    parser.add_argument('-H', '--height', default=HEIGHT, type=int, help="Captured image height (pixels)")
    parser.add_argument('-m', '--maxsize', action="store_true", help="Ignore WIDTH and HEIGHT and use the maximum size")
    parser.add_argument('-f', '--format', type=str, default=DEFAULT_FMT, choices=['ppm', 'jpg', 'png'], help="Output image file format")
    args = parser.parse_args()
    size = None if args.maxsize else args.width, args.height
    app = App(args.output, format=args.format, size=size)
    app.main_loop()
