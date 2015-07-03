''' Shows the probability of hand rotation between successive frames.'''

import Leap, sys, thread, time,cv2,ctypes
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']    
    
    def on_init(self, controller):
        print "Initialized"
        controller.set_policy(Leap.Controller.POLICY_IMAGES)
        
    def on_connect(self, controller):
        print "Connected"

       # Enable gestures
       # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
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
        interactionBox = frame.interaction_box
        hand = frame.hands.rightmost
        print interactionBox.height, interactionBox.width, interactionBox.depth,interactionBox.center

 
                                        
def main():
    listener = SampleListener()
    controller = Leap.Controller()
    controller.add_listener(listener)
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()
