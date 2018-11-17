import Leap
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xlim=(-500, 500), ylim=(-500, 500), zlim=(-500, 500))
h1, = ax.plot([], [], [], linestyle="", marker="o")

fingersPosX = np.array([0, 0, 0, 0, 0], dtype='float')
fingersPosY = np.array([0, 0, 0, 0, 0], dtype='float')
fingersPosZ = np.array([0, 0, 0, 0, 0], dtype='float')

def init():
	h1.set_data(fingersPosX, fingersPosY)
	h1.set_3d_properties(fingersPosZ)
	return [h1]

def animate(fn,controller):
	frame = controller.frame()
	hand = frame.hands.rightmost
	fingers = hand.fingers
	for finger in (fingers):
		fingersPosX[finger.type] = finger.stabilized_tip_position.x
		fingersPosY[finger.type] = finger.stabilized_tip_position.y
		fingersPosZ[finger.type] = finger.stabilized_tip_position.z
	h1.set_data(fingersPosX, fingersPosY)
	h1.set_3d_properties(fingersPosZ)
	return [h1]

def main():
	controller = Leap.Controller()
	controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
	anim = animation.FuncAnimation(fig, animate, fargs=(controller,), init_func = init, interval=1, blit=True)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
