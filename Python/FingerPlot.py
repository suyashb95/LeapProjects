import Leap
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

controller = Leap.Controller()
controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', xlim=(-300, 400), ylim=(-200, 400), zlim=(-300, 300))
ax.view_init(elev=10., azim=250)

points = np.zeros((3, 6))
colors = np.array([100, 100, 100, 100, 100, 500])

patches = ax.scatter(points[0], points[1], points[2], c='red', s=[20, 20, 20, 20, 20, 50])

def get_points():
	frame = controller.frame()
	hand = frame.hands.rightmost
	if not hand.is_valid: return np.array(patches._offsets3d)
	fingers = hand.fingers
	X = [finger.stabilized_tip_position.x for finger in fingers]
	X.append(hand.palm_position.x)
	Y = [finger.stabilized_tip_position.y for finger in fingers]
	Y.append(hand.palm_position.y)
	Z = [finger.stabilized_tip_position.z for finger in fingers]
	Z.append(hand.palm_position.z)
	return np.array([X, Z, Y])

def plot_points():
	points = get_points()
	patches.set_offsets(points[:2].T)
	patches.set_3d_properties(points[2], zdir='z')
	patches.set_array(colors)

def init():
	plot_points()
	return patches,

def animate(i):
	plot_points()
	return patches,

def main():
	anim = animation.FuncAnimation(fig, animate, init_func=init, blit=False, frames=360, interval=20)
	try:
		plt.show()
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == '__main__':
	main()
