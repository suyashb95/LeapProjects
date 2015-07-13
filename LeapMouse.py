from Controllers.FingerController import FingerListener
import Leap
import sys

def main():
    listener = FingerListener()
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    config = controller.config
    config.set("Gesture.Circle.MinRadius",100.0)
    config.set("Gesture.Circle.MinArc",30 * Leap.PI)
    controller.add_listener(listener)       
    print "Press Enter to exit.."        
    sys.stdin.readline()
    controller.remove_listener(listener)  
    
main()