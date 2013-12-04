cv
==

Computer Vision playground


Requirements:
- OpenCV
- requests

This project contains computer vision algorithms I experiment with.

At the moment, it mainly consists of a few command line utilities which can allow building a supervised machine learning face recognition system.

1. Collect pictures of faces using getfaces.py
The input can be a folder with pictures, a webcam stream, a video file, or the Bing image API.
To use the Bing API, an account must be created and a (free) MS key placed in the local_settings.py file.

2. Optionally tidy up the data.
The Haar Cascade face recognition used is pretty good, but for better results cleaning up the data is always preferable.
annotate.py provides a (very) minimalistic UI to manually annotate collected pictures.

3. Train the classifier
Give train.py a list of folders, each containing a different type of content.
