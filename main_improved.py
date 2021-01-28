import cv2
import sys
import json
import time
import signal
import serial
import random
import threading
from repeatTimer import RepeatTimer
from PIL import Image
import pytesseract
import read_ultrasonics_sensors as sensors
import numpy as np
import decision_making as decision
import signdetv2 as detected
import improved_traffic as lights
from gopigo import *



def fast_worker(running, ser, close_program):
    
    global ROBOT_STATE, robot_speed, distance, direction, initial_encoders, made_turn
    
    is_stopped = False
    
    # count timing to print the state of the ultrasonic sensors
    count_seconds = 0
    t = 0
    while running:
        print("ROBOT'S STATE: ", ROBOT_STATE)
        
    
        # Get data from ultrasonic sensors
        arduino_ultrasonic_data = sensors.get_data_from_arduino(ser)
        
        if arduino_ultrasonic_data:
            # Extract the ultrasonic values
            front_dist = arduino_ultrasonic_data['front_us1']
            left_dist = arduino_ultrasonic_data['left_us1']
            right_dist = arduino_ultrasonic_data['right_us1']
            
            count_seconds += 1
            if count_seconds == 5:
                print(arduino_ultrasonic_data)
                count_seconds = 0
            
            
            if ROBOT_STATE == "INITIAL":
#                 pass
                if not is_stopped:
                    #sign_detecting(frame)
                   # If there is enough space to turn right or left or go forward
                    if made_turn and time.time() < t:
                        fwd()
                    elif made_turn:
                        made_turn = False
                        
                    if left_dist > 300 and right_dist > 300 and front_dist > 300:
                        set_speed(40)
                        robot_speed = 40
                        time.sleep(2.5)
                        decision.lrf_decision(left_dist, right_dist, front_dist, robotWidth)
                        t = time.time() + 3
                        made_turn = True

                    # Going to the LEFT  or RIGHT
                    elif left_dist > 300 and front_dist > 300:
                        set_speed(40)
                        robot_speed = 40
                        time.sleep(2.5)
                        decision.lf_decision(left_dist, right_dist, front_dist, robotWidth)
                        t = time.time() + 3
                        made_turn = True
#                         
                    # Going to the RIGHT or FRONT
                    elif right_dist > 300 and front_dist > 300:
                        set_speed(40)
                        robot_speed = 40
                        time.sleep(2.5)
                        decision.rf_decision(left_dist, right_dist, front_dist, robotWidth)
                        t = time.time() + 3
                        made_turn = True
                    
                    # Going to the left or right
                    elif left_dist > 300 and right_dist > 300:
                        set_speed(40)
                        robot_speed = 40
                        time.sleep(2.5)
                        if front_dist < 90:
                            decision.lr_decision(left_dist, right_dist, front_dist, robotWidth)
                            t = time.time() + 3
                            made_turn = True
                    elif left_dist > 300:
                        set_speed(40)
                        robot_speed = 40
                        time.sleep(0.3)
                        if front_dist < 90:
                            left_rot()
                            time.sleep(1.71)
                            t = time.time() + 3
                            made_turn = True
                    elif right_dist > 300:
                        set_speed(40)
                        robot_speed = 40
                        time.sleep(0.3)
                        if front_dist < 90:
                            right_rot()
                            time.sleep(1.71)
                            t = time.time() + 3
                            made_turn = True
                    else:
                        if right_dist < 140 and left_dist < 140:
                            e = (right_dist - left_dist) / 2
                            k = int(1.3 * e)
                            set_right_speed(robot_speed - k)
                            set_left_speed(robot_speed + k)
                        fwd()
                    
            if ROBOT_STATE == "STOPPED":
                stop()
            
            if ROBOT_STATE == "PROCESSING_DATA":
                pass
            
            if ROBOT_STATE == "DRIVING":
                pass
            
            if ROBOT_STATE == "DRIVING_ACCORDING_SIGNS":
                set_speed(40)
                current_enc = enc_read(1)
                if (current_enc - initial_encoders) < distance and front_dist > 100:
                    if right_dist < 150 and left_dist < 150:
                        e = (right_dist - left_dist) / 2
                        k = int(1.3 * e)
                        set_right_speed(robot_speed - k)
                        set_left_speed(robot_speed + k)
                    fwd()
                else:
                    set_speed(40)
<<<<<<< HEAD
                    fwd()
                    if front_dist < 120:
                        if direction == "R" and right_dist > 300:
                            right_rot()
                            print("turning right")
                            time.sleep(1.71)
                            motor_fwd()
                        elif direction == "L" and left_dist > 300:
                            left_rot()
                            print("turning left")
                            time.sleep(1.71)
                            motor_fwd()
                        t = time.time() + 3
                        ROBOT_STATE = "INITIAL"
                        made_turn = True
=======
                    if direction == "R" and right_dist > 200:
                        right_rot()
                        print("turning right")
                        time.sleep(1.81)
                        motor_fwd()
                    elif direction == "L" and left_dist > 200:
                        left_rot()
                        print("turning left")
                        time.sleep(1.81)
                        motor_fwd()
                    else:
                        fwd()
            
>>>>>>> beef5600a63e5030a972332177a48219163024e2
            
        if not ser.is_open:
            close_program("Serial is closed!")

        time.sleep(0.02)
        
    close_program ()

start_time = time.time() + 2
def slow_worker():
    global ROBOT_STATE, distance, direction, initial_encoders, start_time, robot_speed
    ret, frame = cap.read()
    
#     if frame == None:
#         raise Exception("Couldn't load the frame")
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = frame[100:300, 180:460]
    detected_light = lights.traffic_lights(frame)
    if detected_light == "red":
        ROBOT_STATE = "STOPPED"
        print(detected_light)
        stop()
    elif detected_light == "green":
        print(detected_light)
        ROBOT_STATE = "INITIAL"
    elif detected_light == "blue":
        driving_directions = detected.detect_sign(frame)
#         print("DIRECTIONS ====>  ", driving_directions)

        if driving_directions != 0 and driving_directions != None and ROBOT_STATE == "INITIAL":
            if type(driving_directions) == int:
                set_speed(driving_directions)
                robot_speed = driving_directions
                print("CHANGED SPEED ====> ", driving_directions)
            else:
                ROBOT_STATE = "DRIVING_ACCORDING_SIGNS"
                text = list(driving_directions)
                distance = int(text[0]) * 10
                direction = text[1]
                initial_encoders = enc_read(1)
        else:
            pass
        
    cv2.imshow("blue", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return -1
    
    return



def close_program(message=""):
    """
    line_following specific cleanup function
    """
    global running, ser, timer
    print(message)
    running = False
    stop()
    if ser.is_open:
        ser.close()
    timer.cancel()
    if fast_thread.is_alive:
        try:
            fast_thread.join()
        except:
            pass
    
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
    
    
    # Direction and decionmaking variables
    robotWidth = 15

    # Variables for sign detection
    found = False
    turning = ["2R", "3R", "4R", "5R", "6R", "2L", "3L", "4L", "5L", "6L"]


    # variables for sign detecting state
    distance = 0
    direction = 0
    initial_encoders = 0
    
    # Robot default speed
    robot_speed = 40
    set_speed(robot_speed)
    
    # Defining Robot initial state
    ROBOT_STATE = "INITIAL"
    made_turn = False

    # Initialize the camera
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)



    running, ser = sensors.initialize_serial('/dev/ttyUSB0')

    
    
    # create fast worker in a separeate thread
    fast_thread = threading.Thread(
        target=fast_worker,
        args=(running, ser, close_program)
        )
    
    fast_thread.daemon = True
    fast_thread.start()
    
    timer = RepeatTimer(0.1, slow_worker)
    timer.start()
    
    while running:
        time.sleep(1)
    close_program()
    
    

    
            
          


#cap.release()
#cv2.destroyAllWindows()
#robot.stop()
    
    

