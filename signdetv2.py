import cv2
import numpy as np
from PIL import Image
import pytesseract


#has_detected_blue_sign = False
found = False
turning = ["2R", "3R", "4R", "5R", "6R", "2L", "3L", "4L", "5L", "6L"]

def parseText(text):
    global turning
    print("TEXT ====>", text)
    for elem in turning:
        if elem in text:
            return elem
    if "SL" in text:
        return "5L"
    if "SR" in text:
        return "5R"
    if "AL" in text:
        return "4L"
    if "AR" in text:
        return "4R"

    try:
        speed = int(text)
        if 200 > speed > 60:
            return speed - 40
        else:
            print("bad read")
            return 0
    except ValueError:
        return 0
            
            
def blue_sign(img):  # threshold blue signs in frame and return the text on the sign if found
    global found
    lowerlimits = np.array([24, 20, 109], np.uint8)
    upperlimits = np.array([255, 255, 237], np.uint8)
    thresholded = cv2.inRange(img, lowerlimits, upperlimits)
    _, contours, hierarchy = cv2.findContours(thresholded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda f: cv2.contourArea(f), reverse=True)
    roi = img
    if len(contours) > 0:
        sign = contours[0]
        print("size: "+str(cv2.contourArea(sign)))
        x, y, w, h = cv2.boundingRect(sign)
        roi = img[int(y):int(y + h), int(x):int(x + w)]
        if 2400 > cv2.contourArea(sign) > 1600:
            found = True
            roi = cv2.cvtColor(roi, cv2.COLOR_HSV2BGR)
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, img_binarized = cv2.threshold(roi, 75, 255, cv2.THRESH_BINARY)
            imgo2 = Image.fromarray(img_binarized)
            result = pytesseract.image_to_string(imgo2, config='--psm 7') # parse the roi for text, treat the text as a single line
            return parseText(result)

    return 0


def detect_sign(frame):
    global found
    
    if not found:
        k = blue_sign(frame)
        return k
    else:
        found = False


if __name__ == "__main__":
    
    cap = cv2.VideoCapture(0)
    cap.release()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
