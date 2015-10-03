A python/C++ project using the Leap Motion API for image processing and gesture control. 

Installation
==========

* Clone the repo or download the zip.
* Make sure you have the Leap SDK installed.
* run `pip install -r "requirements.txt"`
* Follow the instructions [here](https://developer.leapmotion.com/documentation/cpp/devguide/Project_Setup.html)  and [here](http://docs.opencv.org/doc/tutorials/introduction/windows_visual_studio_Opencv/windows_visual_studio_Opencv.html) to get the Leap SDK and OpenCV to work with Visual Studio

Usage
=====

###For LeapMouse

* `cd` to the folder.
* run `python LeapMouse.py`
* The coordinates of the palm are used to move the mouse pointer around.
* A pinch between any finger and the thumb simulates a click.
* If the ring finger and pinky are not extended (Like the German hand gesture for the number three), the script enters scrolling mode and tilting the palm scrolls up and down. Moving the palm front and back zooms into and out of the screen.
* Make a fist with the palm pointing left to grab the active window and move it around the screen.
* Moving the hand in a circle of radius > 50 mm in clockwise/anticlockwise direction increases/decreases the master volume. 
* LeapMouse.py works only with Windows.

###Other scripts

* `cd` to the folder and run `python <script>.py`
* FingerPlot.py uses matplotlib to plot the coordinates of your fingertips.(Needs Numpy and matplotlib)
* ImageCorrection.py uses bilinear interpolation to remove lens distortion from the Leap Motion controller's images
* ImageCorrection.cpp does the same thing but is much faster. 

Screenshots
===========

![alt tag](http://i.imgur.com/sWlKL9V.png)

Right hand image

![alt tag](http://i.imgur.com/gv2TEJP.png)

Left hand image

![alt tag](http://i.imgur.com/sksnwyT.png)

Disparity map

![alt tag](http://i.imgur.com/7IioUYL.png)

Fingertip locations from FingerPlot.py


Dependencies
-----------------

* Pywin32 - Win32 API for Python
* comtypes - Pure Python COM package

Contributing
---------------

All contributions are welcome
