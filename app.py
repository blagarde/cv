#!/usr/bin/env python
import sys
import cv2

video_uri = "http://192.168.1.7:8080/video"    # IP Webcam App
#video_uri = "http://192.168.1.3:8080"    # VLC


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
                self.on_escape()
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

    def on_escape(self):
        raise SystemExit("Clean exit")

    def on_space(self):
        ''' Subclasses welcome to override '''
        print "<space> pressed"

    def get_frame(self):
        success, frame = self.cap.read()
        return self.to_grayscale(frame) if success else None

    def to_grayscale(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        '''
            def main_loop(self):
                capWidth  = int(cv2.GetCaptureProperty(self.cap, cv2.CV_CAP_PROP_FRAME_WIDTH))
                capHeight = int(cv2.GetCaptureProperty(self.cap, cv2.CV_CAP_PROP_FRAME_HEIGHT))
                print 'Started Webcam at resolution ' + str(capWidth) + 'x' + str(capHeight) + '. Press <space> to acquire frame and <ESC> to exit.'
                print 'Files will be saved in', self.ext, 'format in :', self.folder
                # Manually specify capture channels here, depending on hardware (webcam) :
                inputChannels = 3
                capSize = (capWidth, capHeight)
                cv2.SetCaptureProperty(cap, cv2.CV_CAP_PROP_FRAME_WIDTH, capWidth)
                cv2.SetCaptureProperty(cap, cv2.CV_CAP_PROP_FRAME_HEIGHT, capHeight)

            def capture(self):
                img = cv2.QueryFrame(cap)
                resizedImage = cv2.Resize(img, interpolation=cv2.CV_INTER_LINEAR) # Resize to output size
                
                if self.gray =='YES':
                    cv.CvtColor(resizedImage, outputImg, cv.CV_RGB2GRAY)  # Convert to grayscale
                else:
                    outputImg = resizedImage
                        
            def show(self, img):
                cv.ShowImage(win, outputImg) # Display
        '''


CVApp = ComputerVisionApp


if __name__ == "__main__":
    cvapp = CVApp()
    cvapp.main_loop()
