################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time,cv2,ctypes
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


fig = plt.figure()
plt.xlim([0,256])
plt.ylim([0,35000])
line, = plt.plot([],[])
#left = np.ones((240,640),dtype=np.uint8)
#im = plt.imshow(left,vmin = 0,vmax = 255,cmap = 'gray')
def init():
    #im.set_data(np.ones((240,640),dtype=np.uint8))
    line.set_data([],[])
    return  
    
def animate(fn,controller,line):
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
                                     
def main():
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    anim = animation.FuncAnimation(fig,animate,fargs = (controller,line),init_func = init,interval = 1,blit = False,frames = 10)
    plt.show()

if __name__ == "__main__":
    main()
