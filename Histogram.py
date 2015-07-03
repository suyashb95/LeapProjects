'''Plots a live histogram of the images returned by the Leap Motion controller.'''

import Leap, sys, thread, time,cv2,ctypes
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from collections import deque
import math

class RingBuffer():
    def __init__(self, length):
        self.data = np.zeros(length, dtype='f')

    def append(self, x):
        self.data = np.roll(self.data,-1)
        self.data[-1] = x
        
resolution = 50
fig = plt.figure()
plt.xlim([0,resolution-1])
plt.ylim([-2,2])
line, = plt.plot([],[])
line2, = plt.plot([],[])
#left = np.ones((240,640),dtype=np.uint8)
#im = plt.imshow(left,vmin = 0,vmax = 255,cmap = 'gray')
Ydata = deque([0.00]*resolution, maxlen = resolution)
Ydata2 = deque([0.00]*50, maxlen = 50)
#Ydata = RingBuffer(resolution)
#Ydata2 = RingBuffer(resolution)

def init():
    #im.set_data(np.ones((240,640),dtype=np.uint8))
    line.set_data([np.arange(resolution)],[Ydata])
    line2.set_data([np.arange(50)],[Ydata2])
    return  
    
def hist(fn,controller,line):
    images = controller.images
    if images[1].is_valid:  
        image_buffer_ptr0 = images[0].data_pointer
        #image_buffer_ptr1 = images[1].data_pointer
        ctype_array_def = ctypes.c_ubyte * images[0].width * images[0].height
        as_ctype_array0 = ctype_array_def.from_address(int(image_buffer_ptr0))
        #as_ctype_array1 = ctype_array_def.from_address(int(image_buffer_ptr1))        
        left = np.ctypeslib.as_array(as_ctype_array0)
        hist_im = cv2.calcHist([left],[0],None,[256],[0,256])
        #right = np.ctypeslib.as_array(as_ctype_array1)
        #im.set_data(left)
        # if fn == 9:
        #    plt.ylim([0,max(hist_im)])
        line.set_data(np.arange(256),hist_im)
    return 

def plot(fn,controller,line):
    frame = controller.frame()
    if fn == 0:
        lastframe = controller.frame()
    global lastframe
    oldhand = lastframe.hands.rightmost
    hand = frame.hands.rightmost
    if hand:
        fingers = hand.fingers
        thumb = fingers.finger_type(Leap.Finger.TYPE_THUMB)[0]
        #pinky = fingers.finger_type(Leap.Finger.TYPE_PINKY)[0]
        #index = fingers.finger_type(Leap.Finger.TYPE_INDEX)[0]
        if thumb.is_valid:
            #indexPos = index.stabilized_tip_position
            #thumbDir = thumb.direction
            #indexDir = index.direction
            #Distance1 = indexPos.angle_to(hand.direction)
            #Distance2 = indexDir.angle_to(hand.palm_normal)
            Ydata.append(hand.pinch_strength)
            Ydata2.append(oldhand.pinch_strength)
            line.set_ydata(Ydata)
            line2.set_ydata(Ydata)
        return    
                                    
def main():
    controller = Leap.Controller()
    #controller.set_policy(Leap.Controller.POLICY_IMAGES)
    anim = animation.FuncAnimation(fig,plot,fargs = (controller,line),init_func = init,interval = 1,blit = False,frames = 300)
    plt.show()

if __name__ == "__main__":
    main()
