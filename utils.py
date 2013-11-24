import cv2
import os
from config import IMG_FORMATS, DEFAULT_SIZE


def ximages(dirpath, formats=IMG_FORMATS, gray=True):
    """A generator that yields any images found in the input folder"""
    for root, dirs, files in os.walk(dirpath):
        for fn in files:
            ext = fn.split(os.path.extsep)[-1]
            if ext.lower() in formats:
                path = os.path.join(root, fn)
                flags = cv2.CV_LOAD_IMAGE_GRAYSCALE if gray else cv2.CV_LOAD_IMAGE_COLOR
                img = cv2.imread(path, flags=flags)
                if img is not None:
                	yield img


def xresize(img_stream, size=DEFAULT_SIZE, interpolation=cv2.INTER_LINEAR):
    for img in img_stream:
        yield cv2.resize(img, size, interpolation=interpolation)
