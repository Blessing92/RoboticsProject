import cv2
import numpy as np

blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByArea = True
blobparams.minArea = 200
blobparams.maxArea = 2000000
blobparams.minDistBetweenBlobs = 20

blobparams.filterByCircularity = False
blobparams.filterByInertia = False
blobparams.filterByConvexity = False
detector = cv2.SimpleBlobDetector_create(blobparams)


def detect_blobs_red(frame):
    global detector
    """
    Image processing and blob detection logic
    """
    lB = 0
    lG = 184
    lR = 156
    hB = 255
    hG = 255
    hR = 255
    
    lowerLimits = np.array([lB, lG, lR])
    upperLimits = np.array([hB, hG, hR])


    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    thresholded = cv2.bitwise_not(thresholded)
    keypoints = detector.detect(thresholded)


    
    return keypoints

def detect_blobs_blue(frame):
    global detector
    """
    Image processing and blob detection logic
    """
    lowerlimits = np.array([24, 20, 109], np.uint8)
    upperlimits = np.array([255, 255, 237], np.uint8)

    thresholded = cv2.inRange(frame, lowerlimits, upperlimits)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    thresholded = cv2.bitwise_not(thresholded)
    keypoints = detector.detect(thresholded)
    
    return keypoints


def detect_blobs_green(frame):
    global detector
    """
    Image processing and blob detection logic
    """
    lB = 41
    lG = 0
    lR = 23
    hB = 86
    hG = 255
    hR = 255
    
    lowerLimits = np.array([lB, lG, lR])
    upperLimits = np.array([hB, hG, hR])

    thresholded = cv2.inRange(frame, lowerLimits, upperLimits)
    outimage = cv2.bitwise_and(frame, frame, mask = thresholded)
    thresholded = cv2.bitwise_not(thresholded)
    keypoints = detector.detect(thresholded)


    
    return keypoints






# def get_blob_size(keypoints):
#     """
#     Find the size of biggest keypoint
#     """
#     max_size = 0
#     for b in keypoints:
#         if b.size > max_size:
#             max_size = b.size
# 
# 
#     return max_size

# cap = cv2.VideoCapture(0)
def traffic_lights(frame):
    
#     ret, frame = cap.read()
    keypoints = detect_blobs_red(frame)
#     image_with_keypoints = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
#                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    keypoints_g = detect_blobs_green(frame)
#     image_with_keypoints1 = cv2.drawKeypoints(frame, keypoints_g, np.array([]), (0, 0, 255),
#                                              cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    keypoints_b = detect_blobs_blue(frame)
    
    if len(keypoints) > 0 :
        return "red"
    elif len(keypoints_g) > 0:
        return "green"
    elif len(keypoints_b) > 0:
        return "blue"
    else:
        return "neither"
    
#     cv2.imshow("Camera image", image_with_keypoints)
#     cv2.imshow("Camera image", image_with_keypoints1)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         close("Image closed")