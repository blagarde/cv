from utils import ximages, xresize, xvideo, write_to
from facedetect.facedetect import xfaces
from bing import xbing, zbing
from argparse import ArgumentParser
from config import DEFAULT_ROOT, DEFAULT_FMT, IMG_FORMATS


DISPATCH = {
    'folder': ximages,
    'bing': xbing,
    'webcam': xvideo,
    'movie': xvideo
}


def main():
    parser = ArgumentParser(description="Capture faces")
    parser.add_argument('-o', '--output', default=DEFAULT_ROOT, type=str, help="Path to destination folder (must be writable)")
    parser.add_argument('-m', '--method', choices=DISPATCH.keys(), default='folder', help="Type of source to get the faces from")
    parser.add_argument('-n', '--nfaces', type=int, default=None, help="Number of faces to collect")
    parser.add_argument('-f', '--format', type=str, default=DEFAULT_FMT, choices=IMG_FORMATS, help="Output image file format")
    parser.add_argument('source', type=str, help="Single argument, e.g. folder name, search query, webcam URL, video path.")
    args = parser.parse_args()

    method = args.method
    images = DISPATCH[method](args.source)
    if args.nfaces is None and method == 'bing':
        images = zbing  # Safety measure - this one doesn't yield indefinitely

    faces = xfaces(images)
    resized = xresize(faces, size=(64, 64))

    write_to(resized, args.output, format=args.format, limit=args.nfaces)


if __name__ == "__main__":
    main()
