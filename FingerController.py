'''
The palm's coordinates are used to control the mouse pointer, a pinch between a finger and the thumb registers a click.
Uses the circle gesture to control main volume. Clockwise rotation increases the volume whereas anti clockwise rotation decreases it
'''

import Leap
import sys
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
from VolumeTest import volume
import win32api,win32con
from Mouse import Mouse
 
 
def volumeSetter(circle):
    print "Detecting Circle Gesture."
    if circle.radius >= 50 and circle.pointable.tip_velocity > 700:
        level = volume.GetMasterVolumeLevel()
        if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
            print "Clockwise"
            if level + 0.06 < 0:
                print level
                volume.SetMasterVolumeLevel(level + 0.06,None)
        else:
            print "Anti-Clockwise"
            if level - 0.06 > -64:
                print level
                volume.SetMasterVolumeLevel(level - 0.06,None)
                
class FingerListener(Leap.Listener):
    
    def on_init(self, controller):
        print "Initialized"
        self.clicked = 0
        self.mouse = Mouse()
        #controller.set_policy(Leap.Controller.POLICY_IMAGES)
        
    def on_connect(self, controller):
        print "Connected"
       
       #Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
       # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
       # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
       # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"
        
        
    def on_exit(self, controller):
        print "Exited"
                        
    def on_frame(self, controller):
        frame = controller.frame()
        self.mouse.Handler(frame)
                

