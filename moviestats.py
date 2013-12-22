from utils import xvideo
import sys


def getmean(frame_iter):
    ''' Returns the average intensity of frames '''
    mn = 0
    for n, frame in enumerate(frame_iter):
        m = frame.mean()
        mnplus1 = (mn * n + m) / (n + 1)
        mn = mnplus1
    return mn


if __name__ == "__main__":
    path = sys.argv[1]
    print getmean(xvideo(path))

