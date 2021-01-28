
import cv2
import numpy as np
import time

# cap = cv2.VideoCapture(0)
# cap.release()
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)
found = False
stopped = False


def blue_sign(img):  # threshold blue signs in frame and return "True" if sign detected
    global found
    lowerlimits = np.array([24, 78, 151], np.uint8)
    upperlimits = np.array([255, 255, 237], np.uint8)
    thresholded = cv2.inRange(img, lowerlimits, upperlimits)
    moadwdwa, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda f: cv2.contourArea(f), reverse=True)

    if len(contours) > 0:
        sign = contours[0]
        print("size: "+str(cv2.contourArea(sign)))
        if 2650 > cv2.contourArea(sign) > 2500:
            found = True
            return True
    return False


def detect_sign(cap):
    global found, stopped

    _, frame = cap.read()
    _, frame = cap.read()
    _, frame = cap.read()
    
    print("SHAPE:---> ", frame.shape)
    # frame = cv2.GaussianBlur(frame, (9, 9), 0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("yes", frame)
    
    if not found:
        k = blue_sign(frame)
        if k:
            return 1
    else:
        found = False
        return 0
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return -1 

        
