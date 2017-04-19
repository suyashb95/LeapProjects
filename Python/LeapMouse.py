from Controllers.FingerController import FingerListener
import Leap
import sys
import argparse

#parser = argparse.ArgumentParser()
#parser.add_argument('-s','--sensitivity',default = 2, type = int, help = 'Set mouse sensitivity')

def main():
    #args = parser.parse_args()
    controller = Leap.Controller()
    listener = FingerListener()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    config = controller.config
    config.set("Gesture.Circle.MinRadius",100.0)
    config.set("Gesture.Circle.MinArc",30 * Leap.PI)
    controller.add_listener(listener)       
    print("Press Enter to exit..")
    sys.stdin.readline()
    controller.remove_listener(listener)  

if __name__ == '__main__':   
    main()