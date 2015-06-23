'''Uses the circle gesture to control main volume. Clockwise rotation increases the volume whereas anti clockwise rotation decreases it'''

import Leap, sys, thread, time,cv2,ctypes
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
from VolumeTest import volume


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
        for gesture in controller.frame().gestures():
            if gesture.type is Leap.Gesture.TYPE_CIRCLE and gesture.is_valid:
                circle = Leap.CircleGesture(gesture)
                print "Detecting Circle Gesture."
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

 
                                        
def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()
    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
