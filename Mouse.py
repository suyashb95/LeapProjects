import Leap
import win32api,win32con,win32gui

'''
TO DO:
	Use interaction box to fix movement boundaries. //Done
	Make Pointer mode and Scroller mode more accurate.(Use finger directions) //Done 
	Distinguish accurate clicks.(Index and Pinky, use pinch_strength, and angle to, possibly derivative.)
	Use Kalman filters to smoothen movement.
	Miscellaneous gestures.
'''
	

class Mouse():
	
	def __init__(self,interaction_box):
		self.screen_resolution = (win32api.GetSystemMetrics(0),
									win32api.GetSystemMetrics(1))
		self.center  = {'x':self.screen_resolution[0]/2,
						'y':self.screen_resolution[1]/2}
		self.interactionBox = interaction_box
		self.mode = 0
		self.clicked = 0
		self.clickPoint = None
		self.zoomCoord = None
		
	def Handler(self,frame):
		hands = frame.hands
		if hands:
			Hand = None
			for item in hands:
				if item.is_right:
					Hand = item
			fingers = Hand.fingers
			extended_fingers = fingers.extended()
			self.mode = 0
			Ring = fingers.finger_type(3)[0]
			Pinky = fingers.finger_type(4)[0]
			print len(extended_fingers)
			if 2<= len(extended_fingers) <=3:
				if Ring not in extended_fingers and Pinky not in extended_fingers:
					Middle = fingers.finger_type(2)[0]
					pinky_to_mid = Pinky.direction.angle_to(Middle.direction)
					pinky_to_palm = Pinky.direction.angle_to(Hand.direction)
					if 0.1 <= pinky_to_palm <= 3.5 and 0.1 <= pinky_to_mid <= 2.5:
						self.mode = 1
						if self.clickPoint is None:
							self.clickPoint = Hand.palm_position.z
							
			elif len(extended_fingers) == 0:
				if Hand.grab_strength > 0.9:
					self.Pointer(Hand,1)
			if self.mode == 0:
				print "Pointer Mode."
				self.clickPoint = None
				self.zoomCoord = None

				self.Pointer(Hand,0)
			else:
				print "Scroll Mode"
				self.Scroller(Hand)
	
	def Scroller(self,hand):
		handDir = hand.direction
		handPos = hand.palm_position
		pitch = handDir.pitch
		print self.clickPoint,handPos.z
		x,y = win32api.GetCursorPos()
		print win32api.GetAsyncKeyState(win32con.VK_LCONTROL)
		if pitch > 0.2:
			print "Scroll up"
			win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 10, 0)
			return 
		if pitch < -0.2:
			print "Scroll Down"
			win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -10, 0)
			return 
		#self.zoomDetect(handPos.z,self.clickPoint)
				
	def Pointer(self,hand,grab):
		handPos = hand.stabilized_palm_position
		if -300 <= handPos.x <= 300 and 100 <= handPos.y <= 500:  
			x = int(9.6*hand.stabilized_palm_position.x) + self.center['x']
			y = -int(8.1*(hand.stabilized_palm_position.y - 250)) + self.center['y']
			if grab:
				print "Grab Mode"
				win_handle = win32gui.GetForegroundWindow()
				win_size = win32gui.GetWindowRect(win_handle)
				win32gui.MoveWindow(win_handle,x,y,
									win_size[2]- win_size[0],
									win_size[3] - win_size[1],
									False)
				return 
			else:
				win32api.SetCursorPos((x,y))
				if hand.pinch_strength > 0.95 and self.clicked == 0:
					win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
					self.clicked = 1
				if self.clicked == 1:
					if hand.pinch_strength <= 0.95:
						win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
						self.clicked = 0
				return
					
	def zoomDetect(self,z,clickPoint):
		if abs(z - clickPoint) > 20.0:
			print "Zoom"
			if self.zoomCoord is None:
				self.zoomCoord = z
				if (z - clickPoint) > 0.0:
					self.Zoom(-1)
				else:
					self.Zoom(1)
			elif self.zoomCoord - z > 5.0:
				self.Zoom(1)
				print "In"
				self.zoomCoord = z
			elif self.zoomCoord - z < -5.0:
				self.Zoom(-1)
				print "Out"
				self.zoomCoord = z	
				
	def Zoom(self,zoomFactor):
		x,y = win32api.GetCursorPos()
		win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_EXTENDEDKEY, 0)
		if zoomFactor < 0:
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 1, 0)
			win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
		else:
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -1, 0)
			win32api.keybd_event(win32con.VK_LCONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)


			
					 
		
		
			
			
	