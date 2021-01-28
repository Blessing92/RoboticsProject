import cv2
import sys
import json
import time
import signal
import serial
import random
import read_ultrasonics_sensors as sensors
import numpy as np
import decision_making as decision
import signdet as detected
from gopigo import *


# Direction and decionmaking variables

robotWidth = 15
# Robot and Camera Initialization
def initialize():
    global cap, robot_speed
    
    cap = cv2.VideoCapture(0)
    cap.release()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
#     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    set_speed(robot_speed)
    
    return 0



# Thresholding initialization
def thresh():
    
    return 0


def close_program(message=""):
    """
    line_following specific cleanup function
    """
    global running, ser, robot
    print(message)
    running = False
    #robot.stop()
    if ser.is_open:
        ser.close()
    stop()
    sys.exit(0)



# This function will be called when CTRL+C is pressed
def signal_handler(sig, frame):
    """
    This function will be called when CTRL+C is pressed
    """
    close_program('\nYou pressed Ctrl+C! Closing the program nicely :)')



if __name__ == "__main__":
    # Let's Register a callback for CTRL+C
    signal.signal(signal.SIGINT, signal_handler)

    # Global variable for video feed
    cap = None


    # Robot default speed
    robot_speed = 50
    
    # Defining Robot initial state
    ROBOT_STATE = "INITIAL"

    # Initialize parameters
    initialize()

    running, ser = sensors.initialize_serial('/dev/ttyUSB0')

    is_stopped = False
    
    while running:
        print("ROBOT'S STATE: ", ROBOT_STATE)
        
        # Get data from ultrasonic sensors
        arduino_ultrasonic_data = sensors.get_data_from_arduino(ser)
        
        if arduino_ultrasonic_data:
            # Extract the ultrasonic values
            front_dist = arduino_ultrasonic_data['front_us1']
            left_dist = arduino_ultrasonic_data['left_us1']
            right_dist = arduino_ultrasonic_data['right_us1']
            
            print(arduino_ultrasonic_data)
            
            
            if ROBOT_STATE == "INITIAL":
                sign = detected.detect_sign(cap)
                if sign == 1:
                    print("stopping")
                    stop()
                    time.sleep(3)
                    state = True
                     #detected.detect_sign()
                else: 
                    print("CONTINUE MOVING")
                    state = False
           
                
                if not is_stopped:
    #                 # If there is enough space to turn right or left or go forward
                    if left_dist > 100 and right_dist > 100 and front_dist > 100:
                         time.sleep(1.5)
                         decision.lrf_decision(left_dist, right_dist, front_dist, robotWidth)
                         time.sleep(1.5)
                     
                     #if left_dist > 100 and front_dist > 100:
                      #   decision.lf_decision(left_dist, right_dist, front_dist, robotWidth)
    # 
    #                 elif right_dist > 100 and front_dist > 100:
    #                     decision.rf_decision(left_dist, right_dist, front_dist, robotWidth)
    # 
                    if left_dist > 100 and right_dist > 100:
                        #time.sleep(1.3)
                        if front_dist < 90:
                            decision.lr_decision(left_dist, right_dist, front_dist, robotWidth)
                    else:
                        if left_dist > 90:
                            set_left_speed(25)
                            set_right_speed(75)
                            #time.sleep(.05)  
                        elif right_dist > 90:
                            set_right_speed(25)
                            set_left_speed(75)
                            #time.sleep(.05)
                        #if front_dist > 110:
                        set_speed(40)
                        fwd()
                    
                
                    
# 
#                 # Move the robot forward if width is less than or 21 / robot width 15
#                 elif left_dist + right_dist + robotWidth <= 21 and front_dist > 50:
#                     set_speed(50)
#                     motor_fwd()
# 
#                 # Move the robot forward if width is atleast 30 and move faster
#                 elif left_dist + right_dist +  robotWidth >= 30 and front_dist > 50:
#                     set_speed(100)
#                     motor_fwd()
                
#                 if front_dist < 100:
#                     stop()
#                 else:
#                     motor_fwd()
            if ROBOT_STATE == "PROCESSING_DATA":
                pass
            
            if ROBOT_STATE == "DRIVING":
                pass
            
            if ROBOT_STATE == "DRIVING_ACCORDING_SIGNS":
                pass
            
            
        if not ser.is_open:
            close_program("Serial is closed!")

        # Throttle the loop to 50 times per second
        #time.sleep(.02)
            
          
close_program ()

#cap.release()
#cv2.destroyAllWindows()
robot.stop()
    
    
