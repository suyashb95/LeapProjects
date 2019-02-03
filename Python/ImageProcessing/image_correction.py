import ctypes
import sys
import cv2
import Leap
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
from camera_constants import Q, DESTINATION_HEIGHT, DESTINATION_WIDTH
import pyqtgraph.opengl as gl

controller = Leap.Controller()
controller.set_policy(Leap.Controller.POLICY_IMAGES)

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 20
w.show()

g = gl.GLGridItem()

w.addItem(g)

destination = np.empty((DESTINATION_HEIGHT, DESTINATION_WIDTH), dtype=np.ubyte)

stereo_matcher = cv2.StereoBM_create(numDisparities=16*8, blockSize=11)
stereo_matcher.setMinDisparity(-80)
stereo_matcher.setUniquenessRatio(50)

stereo_matcher.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
stereo_matcher.setPreFilterSize(7)
stereo_matcher.setPreFilterCap(50)

stereo_matcher.setSpeckleWindowSize(10)
stereo_matcher.setSpeckleRange(10)

wls_filter = cv2.ximgproc.createDisparityWLSFilter(stereo_matcher)
wls_filter.setLambda(80000)
wls_filter.setSigmaColor(1.2)
right_matcher = cv2.ximgproc.createRightMatcher(stereo_matcher)

def init_distortion_map(image):
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

frame = controller.frame()
images = frame.images
left_x_map, left_y_map = init_distortion_map(frame.images[0])
right_x_map, right_y_map = init_distortion_map(frame.images[1])

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

scatterplot_items = None

def process():
    global map_initialized, scatterplot_items
    frame = controller.frame()
    images = frame.images
    if images[0].is_valid and images[1].is_valid:
        undistorted_left = interpolate(images[0], left_x_map, left_y_map)
        undistorted_right = interpolate(images[1], right_x_map, right_y_map)
        # cv2.imshow('left', undistorted_left)
        # cv2.imshow('right', undistorted_right)
        dispL = np.int16(stereo_matcher.compute(undistorted_left, undistorted_right))
        dispR = np.int16(right_matcher.compute(undistorted_right, undistorted_left))
        filteredDisparity = wls_filter.filter(dispL, undistorted_left, None, dispR)
        depth = cv2.normalize(filteredDisparity, None, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        points = cv2.reprojectImageTo3D(filteredDisparity, Q)
        #cv2.imshow('depth', points)
        if not scatterplot_items:
            scatterplot_items = gl.GLScatterPlotItem(pos=points.reshape(640 * 240, 3), color=(1,1,1,.3), size=0.005, pxMode=False)
            scatterplot_items.rotate(180, 1, 0, 0)
            w.addItem(scatterplot_items)
        else:
            scatterplot_items.setData(pos=points.reshape(640 * 240, 3))

t = QtCore.QTimer()
t.timeout.connect(process)
t.start(20)

def main():
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

if __name__ == '__main__':
    main()
