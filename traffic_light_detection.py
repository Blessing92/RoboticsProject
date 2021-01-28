#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import numpy as np
import cv2
import time


t = time.time()
blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByArea = True
blobparams.minArea = 2000
blobparams.maxArea = 2000000
blobparams.minDistBetweenBlobs = 200

blobparams.filterByCircularity = False
blobparams.filterByInertia = False
blobparams.filterByConvexity = False

detector = cv2.SimpleBlobDetector_create(blobparams)

cv2.namedWindow("Trackbars")
if os.path.exists("/home/niko/robotics-i-loti.05.010-20-21a-b88376-nihat/labs/lab05/trackbar_defaults.txt"):
    f = open("/home/niko/robotics-i-loti.05.010-20-21a-b88376-nihat/labs/lab05/trackbar_defaults.txt")
    f1 = f.readlines()
    lB = int(f1[0].strip())
    lG = int(f1[1].strip())
    lR = int(f1[2].strip())
    hB = int(f1[3].strip())
    hG = int(f1[4].strip())
    hR = int(f1[5].strip())
    f.close()


else:
    lB = 166
    lG = 134
    lR = 115
    hB = 255
    hG = 255
    hR = 255


def updatelB(new_value):
  global lH
  lB = new_value
  return

def updatelG(new_value):
  global lS
  lG = new_value
  return

def updatelR(new_value):
  global lV
  lR = new_value
  return

def updatehB(new_value):
  global hH
  hB = new_value
  return

def updatehG(new_value):
  global hS
  hG = new_value
  return

def updatehR(new_value):
  global hV
  hR = new_value
  return


cv2.createTrackbar("lH", "Trackbars", lB, 255, updatelB)
cv2.createTrackbar("lS", "Trackbars", lG, 255, updatelG)
cv2.createTrackbar("lV", "Trackbars", lR, 255, updatelR)
cv2.createTrackbar("hH", "Trackbars", hB, 255, updatehB)
cv2.createTrackbar("hS", "Trackbars", hG, 255, updatehG)
cv2.createTrackbar("hV", "Trackbars", hR, 255, updatehR)



# open the camera
cap = cv2.VideoCapture(0)

while True:
  #read the image from the camera
  ret, frame = cap.read()
  rt = 1 // (time.time() - t)
  t = time.time()

  #You will need this later
  frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

  frame = cv2.GaussianBlur(frame,(5,5),0)
  #frame = cv2.medianBlur(frame,5)
  # colour detection limits
  #cv2.imshow('Original', frame)
  lowerLimits = np.array([lB, lG, lR])
  upperLimits = np.array([hB, hG, hR])



  # Our operations on the frame come here
  thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
  outimage = cv2.bitwise_and(frame, frame, mask = thresholded)

  cv2.putText(frame, str(rt), (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
  thresholded = cv2.bitwise_not(thresholded)
  keypoints = detector.detect(thresholded)
  for k in keypoints:
    x = round(k.pt[0],2)
    y = round(k.pt[1],2)
    text = "x =" + str(x) + " y =" + str(y)
    cv2.putText(frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
  frame = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
  if len(keypoints) == 1:
        print("red")

  cv2.imshow('Blurred', frame)
  cv2.imshow('Thresh', thresholded)


  # Display the resulting frame
  #cv2.imshow('Processed', outimage)

  # Quit the program when 'q' is pressed
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

# When everything done, release the capture
print('closing program')
cap.release()
cv2.destroyAllWindows()

f = open("/home/niko/robotics-i-loti.05.010-20-21a-b88376-nihat/labs/lab05/trackbar_defaults.txt", "w")
f.write(str(lB) + "\n" + str(lG)+ "\n" + str(lR)+ "\n" + str(hB)+ "\n" + str(hG)+ "\n" + str(hR))
f.close()



# In[ ]:




