#!/usr/bin/env python

import os
import cv2
from app import ComputerVisionApp
from argparse import ArgumentParser
from datetime import datetime

# Definition of output format
outsize = WIDTH, HEIGHT = 80, 60
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ROOT = os.path.join(HERE, 'data')
DEFAULT_FMT = 'ppm'


def now_str():
    return str(datetime.now()).replace(':','').replace(' ','_')

class App(ComputerVisionApp):
    def __init__(self, folder=DEFAULT_ROOT, gray=True, format=DEFAULT_FMT):
        self.folder = folder
        self.channels = 1 if gray else 3
        self.ext = format
        folder = os.path.join(folder, now_str()) if folder == DEFAULT_ROOT else folder
        if not os.path.isdir(folder):
            os.makedirs(folder)
            print "Created:", folder
        self.folder = folder

    def on_space(self):
        frame = self.get_frame()
        now = now_str()
        filename = now + '.' + self.ext
        outpath = os.path.join(self.folder, filename)
        cv2.imwrite(outpath, frame)
        print now, '- Captured frame: ', outpath

if __name__ == "__main__":
    parser = ArgumentParser(description="Open a capture device and save frames to a folder")
    parser.add_argument('-f', '--folder', default=DEFAULT_ROOT, type=str, help="Path to destination folder (must be writable)")
    args = parser.parse_args()
    app = App(args.folder)
    app.main_loop()
