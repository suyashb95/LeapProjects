'''
* The coordinates of the palm are used to move the mouse pointer around.
* A pinch between any finger and the thumb simulates a click.
* If the ring finger and pinky are not extended (Like the German three hand gesture), the script enters scrolling mode and tilting the palm scrolls up and down. Moving the palm front and back zooms into and out of the screen.
* Make a fist with the palm pointing left to grab the active window and move it around the screen.
* Moving the hand in a circle of radius > 50 mm in clockwise/anticlockwise direction increases/decreases the master volume.
'''


import sys
import Leap
from Leap import CircleGesture
import win32api, win32con
from .Mouse import Mouse


class FingerListener(Leap.Listener):

    def on_init(self, controller):
        print("Initialized")
        self.mouse = Mouse()
        #controller.set_policy(Leap.Controller.POLICY_IMAGES)

    def on_connect(self, controller):
        print("Connected")

       #Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
       # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
       # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
       # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")


    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        self.mouse.Handler(controller)



