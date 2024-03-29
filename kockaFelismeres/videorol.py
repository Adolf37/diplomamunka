import cv2
import numpy as np
from collections import deque


def rescaleFrame(frame,scale=0.75):
    #mukodik kepeken, videokon es elo videokon
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)

    return cv2.resize(frame,dimensions, interpolation = cv2.INTER_AREA)

 
min_threshold = 10                      # these values are used to filter our detector.
max_threshold = 200                     # they can be tweaked depending on the camera distance, camera angle, ...
min_area = 100                          # ... focus, brightness, etc.
min_circularity = 0.3
min_inertia_ratio = 0.5
 
cap = cv2.VideoCapture(0)               # '0' is the webcam's ID. usually it's 0/1/2/3/etc. 'cap' is the video object.
cap.set(15, -4)                         # '15' references video's exposure. '-4' sets it.
cap.set(3,1000)
cap.set(4,1000)
 
'''
You can also adjust brightness, contrast, and many other video properties using set().
https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
'''
 
counter = 0                             # script will use a counter to handle FPS.
readings = deque([0, 0], maxlen=10)     # lists are used to track the number of pips.
display = deque([0, 0], maxlen=10)
 
while True:
    ret, im = cap.read()                                    # 'im' will be a frame from the video.
 
    params = cv2.SimpleBlobDetector_Params()                # declare filter parameters.
    params.filterByArea = True
    params.filterByCircularity = True
    params.filterByInertia = True
    params.minThreshold = min_threshold
    params.maxThreshold = max_threshold
    params.minArea = min_area
    params.minCircularity = min_circularity
    params.minInertiaRatio = min_inertia_ratio
 
    detector = cv2.SimpleBlobDetector_create(params)        # create a blob detector object.
    #im_2 = rescaleFrame(im)
    #im_g = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    keypoints = detector.detect(im)                         # keypoints is a list containing the detected blobs.
    #cv2.imshow('Rescale',im_2)
 
    # here we draw keypoints on the frame.
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 255, 0),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #im_with_keypoints_2 = rescaleFrame(im_with_keypoints,1.5)
    cv2.imshow("Dice Reader", im_with_keypoints)            # display the frame with keypoints added.
 
    if counter % 10 == 0:                                   # enter this block every 10 frames.
        reading = len(keypoints)                            # 'reading' counts the number of keypoints (pips).
        readings.append(reading)                            # record the reading from this frame.
 
        if readings[-1] == readings[-2] == readings[-3]:    # if the last 3 readings are the same...
            display.append(readings[-1])                    # ... then we have a valid reading.
 
        # if the most recent valid reading has changed, and it's something other than zero, then print it.
        if display[-1] != display[-2] and display[-1] != 0:
            msg = f"{display[-1]}\n****"
            print(msg)
 
    counter += 1
 
    if cv2.waitKey(1) & 0xff == 27:                          # press [Esc] to exit.
        break

cv2.destroyAllWindows()