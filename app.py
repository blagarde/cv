#!/usr/bin/env python
import sys
import cv2

video_uri = "http://192.168.1.3:8080/video"    # IP Webcam App
video_uri = "http://192.168.1.3:8080"    # VLC


class ComputerVisionApp(object):
    cap = cv2.VideoCapture(video_uri)
    title = "CV App"
    win = cv2.namedWindow(title, 1) 

    def main_loop(self):
        while True:
            frame = self.get_frame()
            cv2.imshow(self.title, frame)
            key = cv2.waitKey(1)
            if key == 27:   # ESC
                raise SystemExit("Clean exit")
            elif key == 32:   # Space
                self.on_space()
            elif key != -1:
                method_name = "do_" + chr(key)
                try:
                    method = getattr(self, method_name)
                except AttributeError:
                    print >> sys.stderr, "e. Invalid key pressed:", chr(key)
                    continue
                method()

    def on_space(self):
        ''' Subclasses welcome to override '''
        print "<space> pressed"

    def get_frame(self):
        success, frame = self.cap.read()
        return self.to_grayscale(frame) if success else None

    def to_grayscale(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

CVApp = ComputerVisionApp


if __name__ == "__main__":
    cvapp = CVApp()
    cvapp.main_loop()
