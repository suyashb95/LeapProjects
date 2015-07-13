A python project using the Leap Motion API for image processing and gesture control. 

##Installation
* Clone the repo or download the zip.
* Make sure you have the Leap SDK installed.
* run `pip install -r "requirements.txt"`

##Usage
* `cd` to the folder.
* run python LeapMouse.py
* The coordinates of the palm are used to move the mouse pointer around.
* A pinch between any finger and the thumb simulates a click.
* If the ring finger and pinky are not extended, the script enters scrolling mode and tilting the palm scrolls up and down, moving the palm front and back zooms into and out of the screen.
* Ball the hand into a fist with the palm pointing left to grab the active window and move it around the screen.
* HandStats.py uses matplotlib to plot characteristics like image histogram or hand coordinates.
* HandDetect.py uses the Leap Image API and OpenCV to detect hands by accessing images from the controller.

###Contributing
All contributions are welcome
