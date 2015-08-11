from Controllers.Windows import Leap
import sys
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

fig = plt.figure()
ax = plt.axes(xlim = (-500,500),ylim = (0,400))
h1, = plt.plot([],[],'ro')
fingersPosX = np.array([0,0,0,0,0],dtype = 'float')
fingersPosY = np.array([0,0,0,0,0],dtype = 'float')

def init():
	h1.set_data(fingersPosX,fingersPosY)
	
def animate(fn,controller):
	frame = controller.frame()
	hand = frame.hands.rightmost
	fingers = hand.fingers
	for finger in (fingers):
		fingersPosX[finger.type()] = finger.stabilized_tip_position.x
		fingersPosY[finger.type()] = finger.stabilized_tip_position.y
	h1.set_data(fingersPosX,fingersPosY)
			
def main():
	controller = Leap.Controller()
	controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
	anim = animation.FuncAnimation(fig,animate,fargs = (controller,),init_func = init, interval = 1,blit = False)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)
		
if __name__ == '__main__':
	main()
