#!/usr/bin/env python
import cv2
import os
from argparse import ArgumentParser


HERE = os.path.abspath(os.path.dirname(__file__))
FACES = os.path.join(HERE, 'haarcascade_frontalface_default.xml')
EYES = os.path.join(HERE, 'haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier(FACES)
eye_cascade = cv2.CascadeClassifier(EYES)


def detect(img):
    return face_cascade.detectMultiScale(img, 1.3, 5)


def xfaces(img_stream):
    """A generator that yields any faces detected in the input images"""
    for img in img_stream:
        faces = detect(img)
        for i, rect in enumerate(faces):
            x, y, w, h = rect
            roi = img[y:y + h, x:x + w]
            yield roi


def draw_faces(gray_img, outpath):
    faces = detect(gray_img)
    for x, y, w, h in faces:
        cv2.rectangle(gray_img, (x, y), (x + w, y + h), (255, 255, 255), 2)
    if len(faces) > 0:
        cv2.imwrite(outpath, gray_img)
        print "Wrote: %s - %i face(s)" % (outpath, len(faces))


if __name__ == "__main__":
    parser = ArgumentParser(description="Scan a folder for images and detect faces in them")
    parser.add_argument('dirname', help="Folder to scan")
    parser.add_argument('-f', '--format', default='ppm', choices=['ppm'], help="Scan for images with this extension")
    parser.add_argument('-o', '--output', default='output', help="Output folder")
    args = parser.parse_args()

    outdir = args.output
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
        print "Created: {d}".format(outdir)

    for root, dirs, files in os.walk(args.dirname):
        for fn in files:
            if fn.endswith(args.format):
                path = os.path.join(root, fn)
                gray = cv2.imread(path, flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)

                outpath = os.path.join(args.output, os.path.basename(path))
                draw_faces(gray, outpath)