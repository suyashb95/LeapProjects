import ctypes
import sys
import cv2
import Leap

import numpy as np

DESTINATION_HEIGHT = 240
DESTINATION_WIDTH = 640

destination = np.empty((DESTINATION_HEIGHT, DESTINATION_WIDTH), dtype=np.ubyte)

def initDistortionMap(image):
    distortion_length = image.distortion_width * image.distortion_height
    xmap = np.zeros(distortion_length // 2, dtype=np.float32)
    ymap = np.zeros(distortion_length // 2, dtype=np.float32)

    for i in range(0, distortion_length, 2):
        xmap[distortion_length // 2 - i // 2 - 1] = image.distortion[i] * DESTINATION_WIDTH
        ymap[distortion_length // 2 - i // 2 - 1] = image.distortion[i + 1] * DESTINATION_HEIGHT
    xmap = np.reshape(xmap, (image.distortion_height, image.distortion_width // 2))
    ymap = np.reshape(ymap, (image.distortion_height, image.distortion_width // 2))

    #resize the distortion map to equal desired destination image size
    expanded_xmap = cv2.resize(xmap, (DESTINATION_WIDTH, DESTINATION_HEIGHT), 0, 0, cv2.INTER_LINEAR)
    expanded_ymap = cv2.resize(ymap, (DESTINATION_WIDTH, DESTINATION_HEIGHT), 0, 0, cv2.INTER_LINEAR)
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
    return cv2.remap(img, xmap, ymap, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)


def process(controller):
    map_initialized = False
    stereo_matcher = cv2.StereoBM_create(numDisparities=16*8, blockSize=5)
    stereo_matcher.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
    stereo_matcher.setPreFilterCap(25)
    stereo_matcher.setMinDisparity(-50)
    stereo_matcher.setUniquenessRatio(15)
    stereo_matcher.setSpeckleWindowSize(150)
    stereo_matcher.setSpeckleRange(20)

    while True:
        frame = controller.frame()
        images = frame.images
        if images[0].is_valid and images[1].is_valid:
            if not map_initialized:
                left_x_map, left_y_map = initDistortionMap(frame.images[0])
                right_x_map, right_y_map = initDistortionMap(frame.images[1])
                map_initialized = True
            undistorted_left = interpolate(images[0], left_x_map, left_y_map)
            undistorted_right = interpolate(images[1], right_x_map, right_y_map)
            cv2.imshow('left', undistorted_left)
            cv2.imshow('right', undistorted_right)
            disparity = stereo_matcher.compute(undistorted_left, undistorted_right, None)
            depth = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
            cv2.imshow('disparity', depth)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def main():
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    try:
        process(controller)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
