from Listeners import *
import Leap
import sys
import argparse

def main():
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    config = controller.config
    config.set("Gesture.Circle.MinRadius", 100.0)
    config.set("Gesture.Circle.MinArc", 30 * Leap.PI)

    pointer = Pointer()
    click_listener = ClickListener()
    grab_listener = GrabListener()
    scroll_listener = ScrollListener()
    volume_control = VolumeControl()

    controller.add_listener(pointer)
    controller.add_listener(click_listener)
    controller.add_listener(grab_listener)
    controller.add_listener(scroll_listener)
    controller.add_listener(volume_control)

    print("Press Enter to exit..")
    sys.stdin.readline()

    controller.remove_listener(pointer)
    controller.remove_listener(click_listener)
    controller.remove_listener(grab_listener)
    controller.remove_listener(scroll_listener)
    controller.remove_listener(volume_control)

if __name__ == '__main__':
    main()