import Leap
import win32api,win32con

class Mouse():
	
	def __init__(self):
		self.screen_resolution = (1920,1080)
		self.center  = {'x':self.screen_resolution[1]/2,
						'y':self.screen_resolution[0]/2}
		self.interactionBox = None
		self.mode = 0
		self.clicked = 0
		
	def Handler(self,frame):
		hands = frame.hands
		if hands:
			hand = None
			for item in hands:
				if item.is_right:
					hand = item
			fingers = hand.fingers.extended()
			print len(fingers)
			self.mode = 0
			if len(fingers) == 2 or len(fingers) == 3:
				self.mode = 1
				for finger in fingers:
					if finger.type in [3,4]:
						self.mode = 0
						break
			if self.mode == 0:
				print "Pointer Mode."
				self.Pointer(hand)
			else:
				print "Scroll Mode"
				self.Scroller(hand)
	
	def Scroller(self,hand):
		print "LOL I'll code this later."		
		
		
	def Pointer(self,hand):
		x = 960 + int(7*hand.stabilized_palm_position.x)
		y = -int(7*hand.stabilized_palm_position.y) + 1280 + 540
		win32api.SetCursorPos((x,y))
		#if hand.pinch_strength > 0.9 and self.clicked == 0:
		#	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
		#	self.clicked = 1
		#if hand.pinch_strength <= 0.9 and self.clicked == 1:
		#	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
		#	self.clicked = 0
		
		
			
			
		