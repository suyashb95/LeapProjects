from FingerController import FingerListener
import Leap
import sys

def main():
    listener = FingerListener()
    controller = Leap.Controller()
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    controller.add_listener(listener)       
    print "Press Enter to exit.."        
    sys.stdin.readline()
    controller.remove_listener(listener)  
    
main()