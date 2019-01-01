import ctypes
import sys
import cv2
import Leap

import numpy as np

DESTINATION_HEIGHT = 240
DESTINATION_WIDTH = 640

board_size = (3, 3)

num_boards = board_size[0] * board_size[1]

destination = np.empty((DESTINATION_HEIGHT, DESTINATION_WIDTH), dtype=np.ubyte)

obj = np.array([np.array((i / board_size[0], i % board_size[0], 0.0), dtype=np.float32) for i in range(num_boards)])
object_points, image_points1, image_points2 = [], [], []

stereocalib_criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, 30, 1e-6)
stereocalib_flags = cv2.CALIB_FIX_INTRINSIC | cv2.CALIB_FIX_FOCAL_LENGTH | cv2.CALIB_FIX_PRINCIPAL_POINT

C1 = np.array([
    [134.6, 0, 327.8],
    [0, 67.4, 120.3],
    [0, 0, 1]
])

C2 = np.array([
    [134.3, 0, 323.2],
    [0, 67.3, 123.4],
    [0, 0, 1]
])

D1 = np.array([[-0.396571, -0.80373126, 0.14070022, -0.24970651, 0.67173672]])
D2 = np.array([[ 0.155679, -1.09981795, 0.19912512, -0.00359546, 0.97444669]])
R = np.array([
    [0.99907293, -0.03373247, -0.02674706],
    [0.02385673, 0.95100281, -0.30826047],
    [0.03583491, 0.30733659, 0.95092591]
])
T = np.array([[1.96287273], [1.64604608], [-1.13382269]])
E = np.array([
    [0.08603522, 1.58415876, 1.21575515],
    [-1.20311093, -0.56501597, -1.83622011],
    [-1.59769235, 1.92222268, -0.56104918]
])
F = np.array([
    [1.11375187e-05, 4.09539717e-04, -3.17347325e-02],
    [-3.10798405e-04, -2.91486869e-04, 7.30982328e-02],
    [6.97613364e-03, -2.96551658e-02, 1.00000000e+00]
])

Q = np.array([
    [1., 0., 0., -280.7162652 ],
    [0., 1., 0. , -118.74788302],
    [0., 0., 0., 67.35],
    [0., 0., 0.35696326, -0.]
])

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
    num_samples = 0
    while True:
        frame = controller.frame()
        images = frame.images
        if images[0].is_valid and images[1].is_valid:
            if not map_initialized:
                left_x_map, left_y_map = initDistortionMap(frame.images[0])
                right_x_map, right_y_map = initDistortionMap(frame.images[1])
                map_initialized = True
            undistorted_left = interpolate(images[0], left_x_map, left_y_map)
            undistorted_right = interpolate(images[1], left_x_map, left_y_map)
            left_bw = cv2.adaptiveThreshold(undistorted_left, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 2)
            right_bw = cv2.adaptiveThreshold(undistorted_right, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 2)
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
                if num_samples > num_boards:
                    break
            cv2.imshow('left', undistorted_left)
            cv2.imshow('right', undistorted_right)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                #cv2.imwrite('left.jpg', undistorted_left)
                #cv2.imwrite('right.jpg', undistorted_right)
                break
    #retval,cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(object_points, image_points1, image_points2, C1, D1, C2, D2, imageSize=(640, 240), flags=stereocalib_flags, criteria=stereocalib_criteria)
    a = cv2.stereoRectify(C1, D1, C2, D2, (640, 240), R, T)
    print(a[-1])

def main():
    controller = Leap.Controller()
    controller.set_policy(Leap.Controller.POLICY_IMAGES)
    try:
        process(controller)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    main()
