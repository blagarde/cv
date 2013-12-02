import os
import sys
import cv2
import socket
import numpy as np
from urllib2 import urlopen, URLError
from cStringIO import StringIO
from config import IMG_FORMATS, DEFAULT_SIZE, DEFAULT_FMT


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


def xvideo(path, gray=False):
    cap = cv2.VideoCapture(path)
    try:
        while(cap.isOpened()):
            ret, frame = cap.read()
            yield cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if gray else frame
    except Exception as e:
        sys.stderr.write("e. %s" % e)
    finally:
        cap.release()


def xweb(urls, maxretries=2):
    for url in urls:
        retries = maxretries
        while retries > 0:
            try:
                url = url.encode('utf8')
                data = urlopen(url).read()
                flike = StringIO(data)
                a = np.asarray(bytearray(flike.read()), dtype=np.uint8)
                img = cv2.imdecode(a, flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
                if img is not None:
                    yield img
                retries = 0
            except (URLError, socket.error) as e:
                print >> sys.stderr, 'w.', url, ':', e
                retries -= 1


def xresize(img_stream, size=DEFAULT_SIZE, interpolation=cv2.INTER_LINEAR):
    for img in img_stream:
        yield cv2.resize(img, size, interpolation=interpolation)


def write_to(img_iter, outdir, format=DEFAULT_FMT, limit=None):
    for i, img in enumerate(img_iter):
        if limit is not None and i >= limit:
            break
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
            print "Created:", outdir
        path = os.path.join(outdir, str(i).zfill(5) + '.' + format)
        cv2.imwrite(path, img)
        sys.stdout.write("\rWrote: %s" % path)
        sys.stdout.flush()
