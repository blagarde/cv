import os
import re
import sys
import cv2
import socket
import numpy as np
import urlparse
from decorators import limitable
from cStringIO import StringIO
from config import IMG_FORMATS, DEFAULT_SIZE, DEFAULT_FMT, MAX_RETRIES, POOL_SIZE
using_gevent = False
try:
    import gevent
    from gevent.pool import Pool
    from gevent import monkey
    monkey.patch_socket()
    monkey.patch_ssl()
    using_gevent = True
except ImportError:
    print >> sys.stderr, "w. Not using gevent. Will be slower."
from urllib2 import urlopen, URLError


@limitable
def ximages(dirpath, formats=IMG_FORMATS, gray=True, checksize=False):
    """A generator that yields any images found in the input folder"""
    sizes = set()
    for root, dirs, files in os.walk(dirpath):
        for fn in files:
            ext = fn.split(os.path.extsep)[-1]
            if ext.lower() in formats:
                path = os.path.join(root, fn)
                flags = cv2.CV_LOAD_IMAGE_GRAYSCALE if gray else cv2.CV_LOAD_IMAGE_COLOR
                img = cv2.imread(path, flags=flags)
                if img is not None:
                    sizes |= set([img.shape])
                    if checksize and len(sizes) > 1:
                        raise ValueError("Folder contains images with different sizes: %s" % dirpath)
                    yield img


@limitable
def xvideo(path, gray=True):
    cap = cv2.VideoCapture(path)
    while True:
        ret, frame = cap.read()
        if not ret:
            raise StopIteration("Frame could not be retrieved")
        yield cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) if gray else frame


def url_encode_non_ascii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)


def iri2uri(iri):
    parts = urlparse.urlparse(iri)
    return urlparse.urlunparse(
        part.encode('idna') if parti == 1 else url_encode_non_ascii(part.encode('utf-8'))
        for parti, part in enumerate(parts)
    )


def get_image(iri):
    retries = 2  # maxretries
    while retries > 0:
        try:
            uri = iri2uri(iri)
            data = urlopen(uri).read()
            flike = StringIO(data)
            a = np.asarray(bytearray(flike.read()), dtype=np.uint8)
            img = cv2.imdecode(a, flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
            return img
        except (URLError, socket.error, UnicodeError) as e:
            print >> sys.stderr, 'w.', uri, ':', e
            retries -= 1


def get_images(iris):
    jobs = [gevent.spawn(get_image, i) for i in iris]
    gevent.joinall(jobs)
    return [j.value for j in jobs if j.value is not None]


def iriopen(iri, retries=MAX_RETRIES):
    '''Takes an Internationalized Resource Identifier and returns the image it points to'''
    while retries > 0:
        try:
            uri = iri2uri(iri)
            data = urlopen(uri).read()
            flike = StringIO(data)
            a = np.asarray(bytearray(flike.read()), dtype=np.uint8)
            img = cv2.imdecode(a, flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
            return img
        except (URLError, socket.error, UnicodeError) as e:
            print >> sys.stderr, 'w.', uri, ':', e
            retries -= 1


@limitable
def xweb(iris):
    for i in iris:
        img = iriopen(i)
        if img is not None:
            yield img


if using_gevent:
    @limitable
    def xweb(iris):
        pool = Pool(POOL_SIZE)
        for img in pool.imap_unordered(iriopen, iris):
            if img is not None:
                yield img


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
