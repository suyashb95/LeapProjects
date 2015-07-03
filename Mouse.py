import Leap
import win32api,win32con

'''
TO DO:
	Use interaction box to fix movement boundaries.
	Make Pointer mode and Scroller mode more accurate.(Use finger directions) //Done 
	Distinguish accurate clicks.(Index and Pinky, use pinch_strength, and angle to, possibly derivative.)
	Use Kalman filters to smoothen movement.
'''
	

class Mouse():
	
	def __init__(self,interaction_box):
		self.screen_resolution = (1920,1080)
		self.center  = {'x':self.screen_resolution[0]/2,
						'y':self.screen_resolution[1]/2}
		self.interactionBox = interaction_box
		self.mode = 0
		self.clicked = 0
		
	def Handler(self,frame):
		hands = frame.hands
		if hands:
			Hand = None
			for item in hands:
				if item.is_right:
					Hand = item
			fingers = Hand.fingers
			extended_fingers = fingers.extended()
			print len(extended_fingers)
			self.mode = 0
			Ring = fingers.finger_type(3)[0]
			Pinky = fingers.finger_type(4)[0]
			if 2<= len(extended_fingers) <=3:
				if Ring not in extended_fingers and Pinky not in extended_fingers:
					Middle = fingers.finger_type(2)[0]
					pinky_to_mid = Pinky.direction.angle_to(Middle.direction)
					pinky_to_palm = Pinky.direction.angle_to(Hand.direction)
					if 0.4 <= pinky_to_palm <= 3.0 and 0.20 <= pinky_to_mid <= 2.2:
						self.mode = 1
			if self.mode == 0:
				print "Pointer Mode."
				self.Pointer(Hand)
			else:
				print "Scroll Mode"
				self.Scroller(Hand)
	
	def Scroller(self,hand):
		handDir = hand.direction
		pitch = handDir.pitch
		x,y = win32api.GetCursorPos()
		if pitch > 0.2:
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, 10, 0)
		if pitch < -0.2:
			win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, x, y, -10, 0)
				
	def Pointer(self,hand):
		handPos = hand.stabilized_palm_position
		print handPos
		if -300 <= handPos.x <= 300 and 100 <= handPos.y <= 500:  
			x = int(9.6*hand.stabilized_palm_position.x) + self.center['x']
			y = -int(8.1*(hand.stabilized_palm_position.y - 250)) + self.center['y']
			win32api.SetCursorPos((x,y))
			if hand.pinch_strength > 0.95 and self.clicked == 0:
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
				self.clicked = 1
			if hand.pinch_strength <= 0.95 and self.clicked == 1:
				win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
				self.clicked = 0
		
		
			
			
		