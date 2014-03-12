cv
==

Computer Vision playground


This project contains computer vision algorithms I experiment with.

At the moment, it mainly consists of a few command line utilities which can allow building a supervised machine learning face recognition system.


## Requirements
- numpy
- OpenCV
- requests
- scikit-learn
- gevent (optional, but recommended for faster web scraping)

## Overview
###I. Collect pictures of faces

getfaces.py grabs images of faces and saves them to an output folder. The input can be a folder with pictures, a webcam stream, a video file, or the Bing image API.
To use the Bing API, an account must be created and a (free) [MS key](https://datamarket.azure.com/account/keys) placed in the local_settings.py file.

###II. Optionally tidy up the data.

The Haar Cascade face recognition used is pretty good, but for better results cleaning up the data is always preferable.
annotate.py provides a (very) minimalistic UI to manually annotate collected pictures.

###III. Train the classifier

Give train.py a list of folders, each containing a different type of content.
train.py can be used either to output a model which can later be used on unknown images, or to measure precision its own precision on the dataset it is provided with.


##Example

###1. Scrape Bing
Scrape 5000 faces of people off Bing Images, and place them in a 'notmyfaces' folder

```
./getfaces.py -n 5000 -m bing people -o notmyfaces
```

###2. Get own faces
Grab 100 pictures of your own face from a folder with pictures of you, and save them to a 'myfaces' folder
```
./getfaces.py -n 100 -m folder path/to/my/selfies -o myfaces

# Alternatively, record them using your webcam
./getfaces.py -n 100 -m webcam /dev/video0 -o myfaces

# Or get your faces from a video stream (Use the 'IP Webcam' android App or VLC to stream)
./getfaces.py -n 100 -m webcam http://192.168.X.X:8080 -o myfaces
```
###3. Train Classifier
Train an SVM classifier that can tell you apart from other people
```
./train.py notmyfaces myfaces

# Or check its precision using 3-fold validation (was 97% on my dataset)
./train.py notmyfaces myfaces -v 3
```
