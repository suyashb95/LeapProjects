import Leap
import win32api,win32con,win32gui,comtypes
from .VolumeTest import endpoint, IID_IAudioEndpointVolume, enumerator

class Mouse():
	def __init__(self):
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
		self.mode = 0
		self.clicked = 0
		self.clickPoint = None
		self.zoomCoord = None
		self.cursor_level = None
		self.sensitivity = 2.5

	def Handler(self, controller):
		current_frame = controller.frame()
		prev_frame = controller.frame(30)
		right_hand = list(filter(lambda x: x.is_right, current_frame.hands))[0]
		if right_hand:
			fingers = right_hand.fingers
			extended_fingers = fingers.extended()
			self.mode = 0
			ring = fingers.finger_type(3)[0]
			pinky = fingers.finger_type(4)[0]
			if 2 <= len(extended_fingers) <= 3:
				if ring not in extended_fingers and pinky not in extended_fingers:
					middle = fingers.finger_type(2)[0]
					pinky_to_mid = pinky.direction.angle_to(middle.direction)
					pinky_to_palm = pinky.direction.angle_to(right_hand.direction)
					if 0.1 <= pinky_to_palm <= 3.5 and 0.1 <= pinky_to_mid <= 2.5:
						self.mode = 1
						if self.clickPoint is None:
							self.clickPoint = right_hand.palm_position.z
			elif right_hand.grab_strength > 0.93 and right_hand.palm_normal.x < -0.6:
				self.mode = 2
			if self.mode == 0:
				#print "Pointer"
				self.clickPoint = None
				self.zoomCoord = None
				self.Pointer(right_hand, 0)
				if self.cursor_level is not None:
					win32api.ShowCursor(self.cursor_level)
			elif self.mode == 1:
				#print "Scroller"
				self.Scroller(right_hand)
				if self.cursor_level is not None:
					win32api.ShowCursor(self.cursor_level)
			elif self.mode == 2:
				self.clickPoint = None
				self.zoomCoord = None
				#print "Grabber"
				self.Pointer(right_hand, 1)
			else:
				pass
		for gesture in current_frame.gestures():
			if gesture.type == Leap.Gesture.TYPE_CIRCLE:
				circle = Leap.CircleGesture(gesture)
				if circle.radius > 50:
					self.volumeSetter(circle)

	def Scroller(self,hand):
		handDir = hand.direction
		handPos = hand.palm_position
		pitch = handDir.pitch
		x,y = win32api.GetCursorPos()
		#print win32api.GetAsyncKeyState(win32con.VK_LCONTROL)
		if pitch > 0.175:
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 10, 0)
			return
		if pitch < -0.2:
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -10, 0)
			return
		self.zoomDetect(handPos.z)

	def Pointer(self, hand, grab):
		if hand.translation_probability > 0.5:
			handPos = hand.stabilized_palm_position
			if -200 <= handPos.x <= 200 and 50 <= handPos.y <= 400:
				x = int(self.sensitivity*self.scale_factor['x']*hand.stabilized_palm_position.x) + self.center['x']
				y = -int(self.sensitivity*self.scale_factor['y']*(hand.stabilized_palm_position.y - 225)) + self.center['y']
				if grab != 0:
					if 20 <= x <= 1900 and 20 <= y <= 1060:
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
				else:
					win32api.SetCursorPos((x,y))
					if hand.pinch_strength > 0.97 and self.clicked == 0:
						win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
						self.clicked = 1
					if hand.pinch_strength <= 0.95 and self.clicked == 1:
						win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
						self.clicked = 0

	def zoomDetect(self,z):
		if abs(z - self.clickPoint) > 30.0:
			#print "Zoom"
			if self.zoomCoord is None:
				self.zoomCoord = z
				if (z - self.clickPoint) > 0.0:
					self.Zoom(-1)
				else:
					self.Zoom(1)
			elif self.zoomCoord - z > 10.0:
				self.Zoom(-1)
				#print "In"
				self.zoomCoord = z
			elif self.zoomCoord - z < -10.0:
				self.Zoom(1)
				#print "Out"
				self.zoomCoord = z

	def Zoom(self,zoomFactor):
		x,y = win32api.GetCursorPos()
		if zoomFactor < 0:
			self.keyPress(win32con.VK_LCONTROL)
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 1, 0)
			self.keyRelease(win32con.VK_LCONTROL)
		else:
			self.keyPress(win32con.VK_LCONTROL)
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -1, 0)
			self.keyRelease(win32con.VK_LCONTROL)

	def keyPress(self,key_code):
		if win32api.GetAsyncKeyState(key_code):
			return
		while not win32api.GetAsyncKeyState(key_code):
			win32api.keybd_event(key_code,0,win32con.WM_KEYDOWN,0)


	def keyRelease(self,key_code):
		if not win32api.GetAsyncKeyState(key_code):
			return
		while win32api.GetAsyncKeyState(key_code):
			win32api.keybd_event(key_code,0,win32con.KEYEVENTF_KEYUP,0)

	def hideCursor(self):
		value = win32api.ShowCursor(False) + 1
		while win32api.ShowCursor(False) > -1:
			win32api.ShowCursor(False)
		return value

	def volumeSetter(self, circle):
		endpoint = enumerator.GetDefaultAudioEndpoint(0,1)
		volume = endpoint.Activate(IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )
		if circle.radius >= 50 and circle.pointable.tip_velocity > 700:
			level = volume.GetMasterVolumeLevel()
			if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
				if level + 0.1 < 0:
					volume.SetMasterVolumeLevel(level + 0.1,None)
			else:
				if level - 0.1 > -64:
					volume.SetMasterVolumeLevel(level - 0.1,None)