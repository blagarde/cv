#!/usr/bin/env python
# -*- coding: latin-1 -*-

import cv
import datetime

# Definition of output format
width = 80
height = 60
extension = 'ppm'
gray='YES'
outputSize = (width, height)
capturedir='data\\20101024 80x60 grayscale Steph Baptiste'

# Create window
win = 'Show Cam'
cv.NamedWindow(win)
cap = cv.CreateCameraCapture(-1)
capWidth  = int(cv.GetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_WIDTH))
capHeight = int(cv.GetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_HEIGHT))
print 'Started Webcam at resolution ' + str(capWidth) + 'x' + str(capHeight) + '. Press <space> to acquire frame and <ESC> to exit.'
print 'Files will be saved in', extension, 'format in :', capturedir

# Manually specify capture channels here, depending on hardware (webcam) :
inputChannels = 3
capSize = (capWidth, capHeight)
cv.SetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_WIDTH, capWidth)
cv.SetCaptureProperty(cap, cv.CV_CAP_PROP_FRAME_HEIGHT, capHeight)

grayImg = cv.CreateImage(capSize, cv.IPL_DEPTH_8U, 1)

if gray=='YES':
	outputChannels = 1
else:
	outputChannels = 3;

resizedImage=cv.CreateImage(outputSize, cv.IPL_DEPTH_8U, inputChannels)
outputImg = cv.CreateImage(outputSize, cv.IPL_DEPTH_8U, outputChannels)


key=0
while key != 27: # Escape key has been pressed
	img = cv.QueryFrame(cap)
	cv.Resize(img, resizedImage, interpolation=cv.CV_INTER_LINEAR) # Resize to output size
	
	if gray =='YES':
		cv.CvtColor(resizedImage, outputImg, cv.CV_RGB2GRAY)  # Convert to grayscale
	else:
		outputImg = resizedImage
		
	key = cv.WaitKey(1)
	cv.ShowImage(win, outputImg) # Display
	if key == 32: # Space key has been pressed
		now = str(datetime.datetime.now()) # Get timestamp
		filename=now.replace(':','') + '.' + extension # Name files
		cv.SaveImage(capturedir+'\\'+filename,outputImg)
		print 'Captured frame at : ' + now + 'and saved it under : ' + filename
