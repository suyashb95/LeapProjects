'''Uses images from the Leap Motion controller and openCV for hand detection'''


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
       # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
       # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
       # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
       # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        images = controller.frame().images
        if images[1].is_valid:    
            image_buffer_ptr0 = images[0].data_pointer
            image_buffer_ptr1 = images[1].data_pointer
            ctype_array_def = ctypes.c_ubyte * images[0].width * images[0].height
            as_ctype_array0 = ctype_array_def.from_address(int(image_buffer_ptr0))
            as_ctype_array1 = ctype_array_def.from_address(int(image_buffer_ptr1))  
            left = np.ctypeslib.as_array(as_ctype_array0)
            right = np.ctypeslib.as_array(as_ctype_array1)
            cv2.imshow("Left",left)
            left = cv2.GaussianBlur(left,(9,9),0)
            #val,thresh = cv2.threshold(left,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            val,thresh = cv2.threshold(left,95,255,cv2.THRESH_BINARY)
            #thresh = cv2.adaptiveThreshold(left,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,17,2)
            cv2.imshow("Threshold",thresh)
            edges = cv2.Canny(thresh,val*0.1,val)
            #print edges
            cv2.imshow("Edges",edges)
            #hist_im = cv2.calcHist([left],[0],None,[256],[0,256])
            #cv2.normalize(hist_im,hist_im,0,255,cv2.NORM_MINMAX)
            #hist = np.int32(np.around(hist_im))
            #h = np.zeros((300,256,3))
            #for x,y in enumerate(hist):
            #   cv2.line(h,(x,0),(x,y),(255,255,255))
            #y = np.flipud(h)
            #cv2.imshow("Histogram",y)
            cv2.waitKey(30)
                                        
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
