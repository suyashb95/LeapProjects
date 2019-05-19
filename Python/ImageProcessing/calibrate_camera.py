import ctypes
import sys
import cv2
import Leap

import numpy as np

from camera_constants import *
from utils import *

board_size = (5, 4)

square_size = 31
num_boards = board_size[0] * board_size[1]

destination = np.empty((DESTINATION_HEIGHT, DESTINATION_WIDTH), dtype=np.ubyte)

obj = np.array([np.array(((i / board_size[0]) * square_size, (i % board_size[0]) * square_size, 0.0), dtype=np.float32) for i in range(num_boards)])
object_points, image_points1, image_points2 = [], [], []

stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 500, 0.00000000001)
stereocalib_flags = cv2.CALIB_USE_INTRINSIC_GUESS | cv2.CALIB_SAME_FOCAL_LENGTH

def process(controller):
    map_initialized = False
    num_images = 0
    num_samples = 0
    while True:
        frame = controller.frame()
        images = frame.images
        if images[0].is_valid and images[1].is_valid:
            if not map_initialized:
                left_x_map, left_y_map = init_distortion_map(frame.images[0])
                right_x_map, right_y_map = init_distortion_map(frame.images[1])
                map_initialized = True
            undistorted_left = undistort(convert_image_format(images[0]), left_x_map, left_y_map)
            undistorted_right = undistort(convert_image_format(images[1]), left_x_map, left_y_map)
            left_bw = cv2.adaptiveThreshold(undistorted_left, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
            right_bw = cv2.adaptiveThreshold(undistorted_right, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 3)
            corners_left = cv2.findChessboardCorners(left_bw, board_size, flags=cv2.CALIB_CB_FILTER_QUADS)
            corners_right = cv2.findChessboardCorners(right_bw, board_size, flags=cv2.CALIB_CB_FILTER_QUADS)
            if corners_left[0] and corners_right[0]:
                cv2.cornerSubPix(left_bw, corners_left[1], (3, 3), (-1, -1), stereocalib_criteria)
                cv2.cornerSubPix(right_bw, corners_right[1], (3, 3), (-1, -1), stereocalib_criteria)
                cv2.drawChessboardCorners(undistorted_left, board_size, corners_left[1], corners_left[0])
                cv2.drawChessboardCorners(undistorted_right, board_size, corners_right[1], corners_right[0])
                image_points1.append(corners_left[1])
                image_points2.append(corners_right[1])
                object_points.append(obj)
                num_samples += 1
                print(num_samples)
                if num_samples > num_boards:
                    break
            cv2.imshow('left', undistorted_left)
            cv2.imshow('right', undistorted_right)
            cv2.imshow('left_bw', left_bw)
            cv2.imshow('right_bw', right_bw)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.imwrite(f'left{num_images}.jpg', left_bw)
                cv2.imwrite(f'right{num_images}.jpg', right_bw)
                num_images += 1
                break

    retval,cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(
        object_points, image_points1, image_points2, C1, D1, C2, D2, imageSize=(640, 240), flags=stereocalib_flags, criteria=stereocalib_criteria
    )

    print("params")
    print(retval,cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F)

    print("reprojection matrix")
    a = cv2.stereoRectify(C1, D1, C2, D2, (640, 240), R, T)
    print(a)

def main():
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    try:
        process(controller)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
