from __future__ import division
import cv2,Leap,math
import ctypes,sys
import numpy as np

destinationHeight = 240
destinationWidth = 640
destination = np.empty((destinationHeight,destinationWidth),dtype = np.ubyte)

def initDistortionMap(image):

    distortion_length = image.distortion_width * image.distortion_height
    xmap = np.zeros(distortion_length/2, dtype=np.float32)
    ymap = np.zeros(distortion_length/2, dtype=np.float32)

    for i in range(0,distortion_length,2):
       xmap[distortion_length/2 - i/2 - 1] = image.distortion[i] * destinationWidth
       ymap[distortion_length/2 - i/2 - 1] = image.distortion[i + 1] * destinationHeight
    xmap = np.reshape(xmap, (image.distortion_height, image.distortion_width/2))
    ymap = np.reshape(ymap, (image.distortion_height, image.distortion_width/2))
    #resize the distortion map to equal desired destination image size
    expanded_xmap = cv2.resize(xmap, (destinationWidth, destinationHeight), 0, 0, cv2.INTER_LINEAR)
    expanded_ymap = cv2.resize(ymap, (destinationWidth, destinationHeight), 0, 0, cv2.INTER_LINEAR)
    return expanded_xmap, expanded_ymap



def interpolate(image, xmap, ymap):
    #wrap image data in numpy array
    i_address = int(image.data_pointer)
    ctype_array_def = ctypes.c_ubyte * image.height * image.width
    # as ctypes array
    as_ctype_array = ctype_array_def.from_address(i_address)
    # as numpy array
    as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
    img = np.reshape(as_numpy_array, (image.height, image.width))

    #remap image to destination
    destination = cv2.remap(img, xmap, ymap, interpolation = cv2.INTER_LINEAR, borderMode = cv2.BORDER_TRANSPARENT)
    return destination
	
    
def process(controller):
    mapInitialized = False
    while(True):
        frame = controller.frame()
        images = frame.images
        if images[0].is_valid and images[1].is_valid:
            if not mapInitialized:
                left_x_map, left_y_map = initDistortionMap(frame.images[0])
                right_x_map, right_y_map = initDistortionMap(frame.images[1])
                mapInitialized = True
            undistortedLeft = interpolate(images[0], left_x_map, left_y_map)
            undistortedRight = interpolate(images[1], right_x_map, right_y_map)
            #cv2.imshow("temp",left_y_map)
            cv2.imshow('left',undistortedLeft)
            cv2.imshow('right',undistortedRight)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
		
			   
def main():
	controller = Leap.Controller()
	controller.set_policy_flags(Leap.Controller.POLICY_IMAGES)
	try:
		process(controller)
	except KeyboardInterrupt:
		sys.exit(0)
		
if __name__ == '__main__':
	main()
	