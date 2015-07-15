A python project using the Leap Motion API for image processing and gesture control. 

##Installation
* Clone the repo or download the zip.
* Make sure you have the Leap SDK installed.
* run `pip install -r "requirements.txt"`

##Usage
* `cd` to the folder.
* run `python LeapMouse.py`
* The coordinates of the palm are used to move the mouse pointer around.
* A pinch between any finger and the thumb simulates a click.
* If the ring finger and pinky are not extended (Like the German hand gesture for the number three), the script enters scrolling mode and tilting the palm scrolls up and down. Moving the palm front and back zooms into and out of the screen.
* Make a fist with the palm pointing left to grab the active window and move it around the screen.
* Moving the hand in a circle of radius > 50 mm in clockwise/anticlockwise direction increases/decreases the master volume. 
* HandStats.py uses matplotlib to plot characteristics like image histogram or hand coordinates.(Needs Numpy and matplotlib)
* HandDetect.py uses the Leap Image API and OpenCV to detect hands by accessing images from the controller.(Needs OpenCV)
* LeapMouse.py works only with Windows.

###Dependencies
* Pywin32 - Win32 API for Python
* comtypes - Pure Python COM package

###Contributing
All contributions are welcome
