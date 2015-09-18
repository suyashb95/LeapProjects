from __future__ import division
import cv2,Leap,math
import ctypes,sys
import numpy as np


destinationHeight = 120
destinationWidth = 320
destination = np.empty((destinationWidth,destinationHeight),dtype = np.ubyte)

def interpolate(image):
	width = image.width
	height = image.height
	raw = image.data
	distortion_buffer = image.distortion
	distortion_width = image.distortion_width
	
	for i in xrange(destinationWidth):
		for j in xrange(destinationHeight):
			calibrationX = 63.0 * (i)/destinationWidth
			calibrationY = 62.0 * (1-j/destinationHeight)
			weightX = calibrationX - math.trunc(calibrationX)
			weightY = calibrationY - math.trunc(calibrationY)
			x1 = math.trunc(calibrationX)
			y1 = math.trunc(calibrationY)
			x2 = x1 + 1
			y2 = y1 + 1
			dX1 = distortion_buffer[x1 * 2 + y1 * distortion_width]
			dX2 = distortion_buffer[x2 * 2 + y1 * distortion_width]
			dX3 = distortion_buffer[x1 * 2 + y2 * distortion_width]
			dX4 = distortion_buffer[x2 * 2 + y2 * distortion_width]
			dY1 = distortion_buffer[x1 * 2 + y1 * distortion_width + 1]
			dY2 = distortion_buffer[x2 * 2 + y1 * distortion_width + 1]
			dY3 = distortion_buffer[x1 * 2 + y2 * distortion_width + 1]
			dY4 = distortion_buffer[x2 * 2 + y2 * distortion_width + 1]
			dX = dX1*(1.0 - weightX)*(1.0 - weightY) + dX2*weightX*(1.0 - weightY) + dX3*(1.0 - weightX)*weightY + dX4*weightX*weightY
			dY = dY1*(1.0 - weightX)*(1.0 - weightY) + dY2*weightX*(1.0 - weightY) + dY3*(1.0 - weightX)*weightY + dY4*weightX*weightY
			if 0.0 <= dX <= 1.0 and 0.0 <= dY <= 1.0:
				denormalizedX = math.trunc(dX * width)
				denormalizedY = math.trunc(dY * height)
				destination[i,j] = raw[denormalizedX + denormalizedY * width]
			else:
				destination[i,j] = 0
	return np.transpose(destination)
    
def process(controller):
	while(True):
		frame = controller.frame()
		image = frame.images[0]
		if image.is_valid:
			#image_buffer_ptr = image.data_pointer
			#ctype_array_def = ctypes.c_ubyte * image.width * image.height 
			#as_ctype_array = ctype_array_def.from_address(int(image_buffer_ptr))
			#as_numpy_array = np.ctypeslib.as_array(as_ctype_array)
			undistorted = interpolate(image)
			#cv2.imshow('c',as_numpy_array)
			cv2.imshow('abc',undistorted)
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
	