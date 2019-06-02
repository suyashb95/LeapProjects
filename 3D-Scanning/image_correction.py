import ctypes
import sys
import cv2
import Leap
import numpy as np
import pcl
from pyqtgraph.Qt import QtCore, QtGui
from camera_constants import *
from utils import *
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

stereo_matcher = cv2.StereoBM_create(numDisparities=80, blockSize=13)
stereo_matcher.setSmallerBlockSize(3)
stereo_matcher.setMinDisparity(-80)
stereo_matcher.setUniquenessRatio(15)
stereo_matcher.setPreFilterType(cv2.STEREO_BM_PREFILTER_NORMALIZED_RESPONSE)
stereo_matcher.setPreFilterSize(31)
stereo_matcher.setPreFilterCap(50)
stereo_matcher.setTextureThreshold(8)
stereo_matcher.setSpeckleWindowSize(5)
stereo_matcher.setSpeckleRange(2)

wls_filter = cv2.ximgproc.createDisparityWLSFilter(stereo_matcher)
wls_filter.setLambda(8000)
wls_filter.setSigmaColor(1.2)
right_matcher = cv2.ximgproc.createRightMatcher(stereo_matcher)

right_rectification_map = cv2.initUndistortRectifyMap(C2, D2, R2, P2, (DESTINATION_HEIGHT, DESTINATION_WIDTH), cv2.CV_16SC2)
left_rectification_map = cv2.initUndistortRectifyMap(C1, D1, R1, P1, (DESTINATION_HEIGHT, DESTINATION_WIDTH), cv2.CV_16SC2)

scatterplot_items = gl.GLScatterPlotItem(pos=np.empty([3, 3]), color=(1,1,1,.3), size=0.05, pxMode=False)
scatterplot_items.rotate(180, 1, 0, 0)
w.addItem(scatterplot_items)

def process():
    frame = controller.frame()
    images = frame.images
    left_x_map, left_y_map = init_distortion_map(images[0])
    right_x_map, right_y_map = init_distortion_map(images[1])
    scatterplot_items = gl.GLScatterPlotItem(pos=np.empty([3, 3]), color=(1,1,1,.3), size=0.05, pxMode=False)
    scatterplot_items.rotate(180, 1, 0, 0)
    w.addItem(scatterplot_items)
    image_count = 0
    points = None
    concatenated_points = None
    store_flag = False
    while True:
        frame = controller.frame()
        images = frame.images
        if images[0].is_valid and images[1].is_valid:
            images = (convert_image_format(frame.images[0]), convert_image_format(frame.images[1]))
            undistorted_left = undistort(images[0], left_x_map, left_y_map)
            undistorted_right = undistort(images[1], right_x_map, right_y_map)
            dispL = np.int16(stereo_matcher.compute(undistorted_left, undistorted_right))
            dispR = np.int16(right_matcher.compute(undistorted_right, undistorted_left))
            filteredDisparity = wls_filter.filter(dispL, undistorted_left, None, dispR)
            reprojected_image = cv2.reprojectImageTo3D(filteredDisparity, Q, handleMissingValues=True)
            points = reprojected_image.reshape(640*240, 3)
            points = points[points[:,2] < 100]
            points = points[points[:,2] > -10]
            points = points[points[:,0] < 7]
            concatenated_points = points if concatenated_points is None else np.vstack((concatenated_points, points))
            image_count += 1
            scatterplot_items.setData(pos=concatenated_points)
            if image_count == 3:
                if store_flag:
                    point_cloud = pcl.PointCloud()
                    point_cloud.from_array(concatenated_points)
                    pcl.save(point_cloud, 'point_cloud.pcd', format='pcd')
                    print('saved point cloud')
                image_count = 0
                concatenated_points = None
                store_flag = False
            cv2.imshow('dummy', undistorted_left)
        if cv2.waitKey(1) & 0xFF == ord('l'):
            store_flag = True

def main():
    try:
        process()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
