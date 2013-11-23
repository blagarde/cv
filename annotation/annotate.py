import cv2
import os
import csv
from argparse import ArgumentParser


DEFAULT_MAPPING = None
DEFAULT_OUTPATH = 'annotation_output.csv'
DEFAULT_FORMAT = 'ppm'
FORMATS = ['ppm']


def scan(dirname, ext):
    for root, dirs, files in os.walk(dirname):
        for filename in files:
            if filename.endswith(ext):
                yield os.path.abspath(os.path.join(root, filename))


def read_mapping(mapping):
    with open(mapping) as fh:
        return dict([row for row in csv.reader(fh)])


def annotate(dirname, format=DEFAULT_FORMAT, mapping=DEFAULT_MAPPING, outpath=DEFAULT_OUTPATH):
    basic = {'y': 'yes', 'n': 'no'}
    key_dct = basic if mapping is None else read_mapping(mapping)

    with open(outpath, 'w') as fh:
        writer = csv.writer(fh)
        for path in scan(dirname, format):
            img = cv2.imread(path)
            cv2.imshow("Annotation UI", img)
            while True:
                key = cv2.waitKey(1)
                if key < 0 or key > 255:
                    continue
                elif key == 27:   # ESC
                    raise SystemExit("User quit", -1)
                elif chr(key) in key_dct:
                    writer.writerow((path, key_dct[chr(key)]))
                    break
    print "Wrote:", outpath


if __name__ == "__main__":
    parser = ArgumentParser(description="Training data annotation UI")
    parser.add_argument('dirname', help="Input folder to scan")
    parser.add_argument('-f', '--format', default=DEFAULT_FORMAT, choices=FORMATS, help="Scan for images with this extension")
    parser.add_argument('-m', '--mapping', default=DEFAULT_MAPPING, help="Optional CSV with key -> label mapping. If not supplied, annotation type is y/n")
    parser.add_argument('-o', '--output', default=DEFAULT_OUTPATH, help="Output filename. Default fields are 'path' and 'y/n'")
    args = parser.parse_args()
    annotate(args.dirname, format=args.format, mapping=args.mapping, outpath=args.output)
