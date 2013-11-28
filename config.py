import os

HERE = os.path.abspath(os.path.dirname(__file__))
IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'jpe', 'jp2', 'png', 'pbm', 'ppm', 'gif', 'pgm', 'tif', 'tiff', 'sr', 'ras']
DEFAULT_SIZE = 400, 300
DEFAULT_ROOT = os.path.join(HERE, 'output')
DEFAULT_FMT = 'ppm'
