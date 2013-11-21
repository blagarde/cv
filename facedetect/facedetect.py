import cv2
import os
from argparse import ArgumentParser

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')


def find_faces(path, outdir):
    gray = cv2.imread(path)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for x, y, w, h in faces:
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), 2)

    if len(faces) > 0:
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        outpath = os.path.join(outdir, os.path.basename(path))
        cv2.imwrite(outpath, gray)
        print "Wrote: %s - %i face(s)" % (outpath, len(faces))


if __name__ == "__main__":
    parser = ArgumentParser(description="Scan a folder for images and detect faces in them")
    parser.add_argument('dirname', help="Folder to scan")
    parser.add_argument('-f', '--format', default='ppm', choices=['ppm'], help="Scan for images with this extension")
    parser.add_argument('-o', '--output', default='output', help="Output folder")
    args = parser.parse_args()

    for root, dirs, files in os.walk(args.dirname):
        for fn in files:
            if fn.endswith(args.format):
                path = os.path.join(root, fn)
                find_faces(path, args.output)
