'''
* The coordinates of the palm are used to move the mouse pointer around.
* A pinch between any finger and the thumb simulates a click.
* If the ring finger and pinky are not extended (Like the German three hand gesture), the script enters scrolling mode and tilting the palm scrolls up and down. Moving the palm front and back zooms into and out of the screen.
* Make a fist with the palm pointing left to grab the active window and move it around the screen.
* Moving the hand in a circle of radius > 50 mm in clockwise/anticlockwise direction increases/decreases the master volume. 
'''

from Windows import Leap
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
                

