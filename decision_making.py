#import cv2
import sys
import json
import time
import signal
import serial
import random
import read_ultrasonics_sensors as sensors
import numpy as np
from gopigo import *
import main_improved

make_decision = True
three_directions = ["Left", "Right", "Forward"]
lr_directions = ["Left", "Right"]
lf_directions = ["Left", "Forward"]
rf_directions = ["Forward", "Right"]

def forward(left_dist, right_dist, front_dist, robotWidth):
    set_speed(40)
    fwd()

def rf_decision(left_dist, right_dist, front_dist, robotWidth):
    global make_decision
    
    # reseting the speed 
    set_speed(40)
    
    if make_decision:
        random_dir = random.choice(rf_directions)
        print("DECISION: ", random_dir)
        make_decision = False
    
    if random_dir == "Forward":
        forward(left_dist, right_dist, front_dist, robotWidth)
        time.sleep(1.81)
        make_decision = True

    elif random_dir == "Right":
        # Spin right 2s
        right_rot()
        time.sleep(1.81)
        fwd()
        make_decision = True
    

def lf_decision(left_dist, right_dist, front_dist, robotWidth):
    global make_decision
    # reseting the speed 
    set_speed(40)
    
    if make_decision:
        random_dir = random.choice(lf_directions)
        print("DECISION: ", random_dir)
        make_decision = False
    
    if random_dir == "Forward":
        forward(left_dist, right_dist, front_dist, robotWidth)
        time.sleep(1.81)
        make_decision = True

    elif random_dir == "Left":
        # Spin left 2s
        left_rot()
        time.sleep(1.81)
        fwd()
        make_decision = True

def lr_decision(left_dist, right_dist, front_dist, robotWidth):
    global make_decision
    
    # reseting the speed 
    set_speed(40)
    
    if make_decision:
        random_dir = random.choice(lr_directions)
        print("DECISION: ", random_dir)
        make_decision = False
    

    if random_dir == "Left":
        # Spin left 2s
        left_rot()
        time.sleep(1.81)
        fwd()
        make_decision = True

    elif random_dir == "Right":
        # Spin right 2s
        right_rot()
        time.sleep(1.81)
        fwd()
        make_decision = True

def lrf_decision(left_dist, right_dist, front_dist, robotWidth):
    global make_decision
    
    # reseting the speed 
    set_speed(40)
    
    if make_decision:
        random_dir = random.choice(three_directions)
        print("DECISION: ", random_dir)
        make_decision = False
    
    if random_dir == "Forward":
        forward(left_dist, right_dist, front_dist, robotWidth)
        time.sleep(1)
        make_decision = True

    elif random_dir == "Left":
        # Spin left 2s
        left_rot()
        time.sleep(1.81)
        fwd()
        make_decision = True

    elif random_dir == "Right":
        # Spin right 2s
        right_rot()
        time.sleep(1.81)
        fwd()
        make_decision = True