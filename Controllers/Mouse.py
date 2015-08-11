from Windows import Leap
import win32api,win32con,win32gui,comtypes
from VolumeTest import endpoint,IID_IAudioEndpointVolume,enumerator
	

class Mouse():
	
	def __init__(self,interaction_box):
		self.screen_resolution = (win32api.GetSystemMetrics(0),
									win32api.GetSystemMetrics(1))
		self.center  = {'x':self.screen_resolution[0]/2,
						'y':self.screen_resolution[1]/2}
		self.interactionBox = interaction_box
		self.scale_factor = {'x':self.screen_resolution[0]/400,
							'y': self.screen_resolution[1]/350}
		self.mode = 0
		self.clicked = 0
		self.clickPoint = None
		self.zoomCoord = None
		self.cursor_level = None
		
	def Handler(self,frame):
		hands = frame.hands
		if hands:
			Hand = None
			for item in hands:
				if item.is_right:
					Hand = item
			if Hand:
				fingers = Hand.fingers
				extended_fingers = fingers.extended()
				self.mode = 0
				Ring = fingers.finger_type(3)[0]
				Pinky = fingers.finger_type(4)[0]
				if 2<= len(extended_fingers) <=3:
					if Ring not in extended_fingers and Pinky not in extended_fingers:
						Middle = fingers.finger_type(2)[0]
						pinky_to_mid = Pinky.direction.angle_to(Middle.direction)
						pinky_to_palm = Pinky.direction.angle_to(Hand.direction)
						if 0.1 <= pinky_to_palm <= 3.5 and 0.1 <= pinky_to_mid <= 2.5:
							self.mode = 1	
							if self.clickPoint is None:
								self.clickPoint = Hand.palm_position.z	
								#self.cursor_level = self.hideCursor()
				elif Hand.grab_strength > 0.93 and Hand.palm_normal.x < -0.6:
					self.mode = 2
				else:
					pass
					
				if self.mode == 0:
					#print "Pointer"
					self.clickPoint = None
					self.zoomCoord = None
					self.Pointer(Hand,0)
					if self.cursor_level is not None:
						win32api.ShowCursor(self.cursor_level)
				elif self.mode == 1:
					#print "Scroller"
					self.Scroller(Hand)
					if self.cursor_level is not None:
						win32api.ShowCursor(self.cursor_level)
				elif self.mode == 2:
					self.clickPoint = None
					self.zoomCoord = None
					#print "Grabber"
					self.Pointer(Hand,1)
				else:
					pass
		for gesture in frame.gestures():
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
				
	def Pointer(self,hand,grab):
		handPos = hand.stabilized_palm_position
		if -200 <= handPos.x <= 200 and 50 <= handPos.y <= 400:  
			x = int(2*self.scale_factor['x']*hand.stabilized_palm_position.x) + self.center['x']
			y = -int(2*self.scale_factor['y']*(hand.stabilized_palm_position.y - 225)) + self.center['y']
			if grab != 0:
				if 20 <= x <= 1900 and 20 <= y <= 1060:
					win_handle = win32gui.GetForegroundWindow()
					win_size = win32gui.GetWindowRect(win_handle)
					win32gui.SetWindowPos(win_handle,win32con.HWND_TOP,
										x,y,
										win_size[2]- win_size[0],
										win_size[3] - win_size[1],
										win32con.SWP_NOSIZE)
					return 
			else:
				win32api.SetCursorPos((x,y))
				if hand.pinch_strength > 0.97 and self.clicked == 0:
					win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
					self.clicked = 1
				if hand.pinch_strength <= 0.95 and self.clicked == 1:
					win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
					self.clicked = 0
				return
					
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
		
	def volumeSetter(self,circle):
		endpoint = enumerator.GetDefaultAudioEndpoint(0,1)
		volume = endpoint.Activate( IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )
		if circle.radius >= 50 and circle.pointable.tip_velocity > 700:
			level = volume.GetMasterVolumeLevel()
			if (circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2):
				if level + 0.1 < 0:
					volume.SetMasterVolumeLevel(level + 0.1,None)
			else:
				if level - 0.1 > -64:
					volume.SetMasterVolumeLevel(level - 0.1,None)
			
					 
		
		
			
			
	