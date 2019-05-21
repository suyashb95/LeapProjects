'''
* The coordinates of the palm are used to move the mouse pointer around.
* A pinch between any finger and the thumb simulates a click.
* If the ring finger and pinky are not extended (Like the German three hand gesture), the script enters scrolling mode and tilting the palm scrolls up and down. Moving the palm front and back zooms into and out of the screen.
* Make a fist with the palm pointing left to grab the active window and move it around the screen.
* Moving the hand in a circle of radius > 50 mm in clockwise/anticlockwise direction increases/decreases the master volume.
'''


import sys
import Leap
from Leap import CircleGesture
import win32api, win32con, win32gui, comtypes
from VolumeTest import endpoint, IID_IAudioEndpointVolume, enumerator

class ClickListener(Leap.Listener):
    def on_init(self, controller):
        self.num_monitors = win32api.GetSystemMetrics(80)
        self.sensitivity = 2.5
        self.screen_resolution = (
            win32api.GetSystemMetrics(59),
            win32api.GetSystemMetrics(60)
        )
        self.center  = {
            'x':self.screen_resolution[0]/2,
            'y':self.screen_resolution[1]/2
        }
        self.scale_factor = {
            'x':self.screen_resolution[0]/400,
            'y':self.screen_resolution[1]/350
        }
        self.clicked = 0

    def on_frame(self, controller):
        frame = controller.frame()
        right_hand = list(filter(lambda x: x.is_right, frame.hands))
        if right_hand:
            right_hand = right_hand[0]
            if right_hand.grab_strength < 0.93:
                right_hand_pos = right_hand.stabilized_palm_position
                x = int(self.sensitivity*self.scale_factor['x']*right_hand_pos.x) + self.center['x']
                y = -int(self.sensitivity*self.scale_factor['y']*(right_hand_pos.y - 225)) + self.center['y']
                if right_hand.pinch_strength > 0.97 and self.clicked == 0:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
                    self.clicked = 1
                if right_hand.pinch_strength <= 0.95 and self.clicked == 1:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
                    self.clicked = 0

class Pointer(Leap.Listener):
    def on_init(self, controller):
        self.num_monitors = win32api.GetSystemMetrics(80)
        self.screen_resolution = (
            win32api.GetSystemMetrics(59),
            win32api.GetSystemMetrics(60)
        )
        self.center  = {
            'x':self.screen_resolution[0]/2,
            'y':self.screen_resolution[1]/2
        }
        self.scale_factor = {
            'x':self.screen_resolution[0]/400,
            'y':self.screen_resolution[1]/350
        }
        self.sensitivity = 2.5

    def on_frame(self, controller):
        frame = controller.frame()
        right_hand = list(filter(lambda x: x.is_right, frame.hands))
        if right_hand:
            right_hand = right_hand[0]
            if right_hand.translation_probability > 0.5:
                right_hand_pos = right_hand.stabilized_palm_position
                x = int(self.sensitivity*self.scale_factor['x']*right_hand_pos.x) + self.center['x']
                y = -int(self.sensitivity*self.scale_factor['y']*(right_hand_pos.y - 225)) + self.center['y']
                win32api.SetCursorPos((x,y))

class GrabListener(Leap.Listener):
    def on_init(self, controller):
        self.num_monitors = win32api.GetSystemMetrics(80)
        self.screen_resolution = (
            win32api.GetSystemMetrics(59),
            win32api.GetSystemMetrics(60)
        )
        self.center  = {
            'x':self.screen_resolution[0]/2,
            'y':self.screen_resolution[1]/2
        }
        self.scale_factor = {
            'x':self.screen_resolution[0]/400,
            'y':self.screen_resolution[1]/350
        }
        self.sensitivity = 2.5

    def on_frame(self, controller):
        frame = controller.frame()
        right_hand = list(filter(lambda x: x.is_right, frame.hands))
        if right_hand:
            right_hand = right_hand[0]
            if right_hand.grab_strength > 0.93 and right_hand.palm_normal.x < -0.6:
                right_hand_pos = right_hand.stabilized_palm_position
                x = int(self.sensitivity*self.scale_factor['x']*right_hand_pos.x) + self.center['x']
                y = -int(self.sensitivity*self.scale_factor['y']*(right_hand_pos.y - 225)) + self.center['y']
                win_handle = win32gui.GetForegroundWindow()
                win_size = win32gui.GetWindowRect(win_handle)
                win32gui.SetWindowPos(
                    win_handle,win32con.HWND_TOP,
                    x,
                    y,
                    win_size[2]- win_size[0],
                    win_size[3] - win_size[1],
                    win32con.SWP_NOSIZE
                )

class ScrollListener(Leap.Listener):
    def on_init(self, controller):
        self.num_monitors = win32api.GetSystemMetrics(80)
        self.screen_resolution = (
            win32api.GetSystemMetrics(59),
            win32api.GetSystemMetrics(60)
        )
        self.center  = {
            'x':self.screen_resolution[0]/2,
            'y':self.screen_resolution[1]/2
        }
        self.scale_factor = {
            'x':self.screen_resolution[0]/400,
            'y':self.screen_resolution[1]/350
        }
        self.sensitivity = 2.5

    def on_frame(self, controller):
        frame = controller.frame()
        right_hand = list(filter(lambda x: x.is_right, frame.hands))
        if right_hand:
            right_hand = right_hand[0]
            fingers = right_hand.fingers
            extended_fingers = fingers.extended()
            ring = fingers.finger_type(3)[0]
            pinky = fingers.finger_type(4)[0]
            if 2 <= len(extended_fingers) <= 3:
                if ring not in extended_fingers and pinky not in extended_fingers:
                    middle = fingers.finger_type(2)[0]
                    pinky_to_mid = pinky.direction.angle_to(middle.direction)
                    pinky_to_palm = pinky.direction.angle_to(right_hand.direction)
                    if 0.1 <= pinky_to_palm <= 3.5 and 0.1 <= pinky_to_mid <= 2.5:
                        hand_dir = right_hand.direction
                        hand_pos = right_hand.palm_position
                        pitch = hand_dir.pitch
                        x, y = win32api.GetCursorPos()
                        if pitch > 0.175:
                            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 10, 0)
                        if pitch < -0.2:
                            win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -10, 0)

class VolumeControl(Leap.Listener):
    def on_init(self, controller):
        self.num_monitors = win32api.GetSystemMetrics(80)
        self.screen_resolution = (
            win32api.GetSystemMetrics(59),
            win32api.GetSystemMetrics(60)
        )
        self.center  = {
            'x':self.screen_resolution[0]/2,
            'y':self.screen_resolution[1]/2
        }
        self.scale_factor = {
            'x':self.screen_resolution[0]/400,
            'y':self.screen_resolution[1]/350
        }

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)

    def on_frame(self, controller):
        for gesture in controller.frame().gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = Leap.CircleGesture(gesture)
                if circle.radius > 50:
                    self.set_volume(circle)

    def set_volume(self, circle):
        endpoint = enumerator.GetDefaultAudioEndpoint(0,1)
        volume = endpoint.Activate(IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )
        if circle.radius >= 50 and circle.pointable.tip_velocity > 700:
            level = volume.GetMasterVolumeLevel()
            if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
                if level + 0.1 < 0:
                    volume.SetMasterVolumeLevel(level + 0.1, None)
            else:
                if level - 0.1 > -64:
                    volume.SetMasterVolumeLevel(level - 0.1, None)