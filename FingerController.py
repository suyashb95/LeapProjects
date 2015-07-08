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
    if circle.radius >= 50 and circle.pointable.tip_velocity > 700:
        level = volume.GetMasterVolumeLevel()
        if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
            if level + 0.1 < 0:
                volume.SetMasterVolumeLevel(level + 0.1,None)
        else:
            if level - 0.1 > -64:
                volume.SetMasterVolumeLevel(level - 0.1,None)
                
class FingerListener(Leap.Listener):
    
    def on_init(self, controller):
        print "Initialized"
        self.clicked = 0
        self.mouse = Mouse(controller.frame().interaction_box)
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
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                if circle.radius > 50:
                    volumeSetter(circle)
                

