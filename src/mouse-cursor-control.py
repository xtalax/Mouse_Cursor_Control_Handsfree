from imutils import face_utils
from utils import *
import numpy as np
import pyautogui as pag
import imutils
import dlib
import cv2
import time
import pickle
from os import path
# Thresholds and consecutive frame length for triggering the mouse action.
MOUTH_AR_THRESH = 0.6
MOUTH_AR_CONSECUTIVE_FRAMES = 4
EYE_AR_THRESH = 0.23
EYE_AR_CONSECUTIVE_FRAMES = 4
WINK_AR_DIFF_THRESH = 0.075
WINK_AR_CLOSE_THRESH = 0.20
WINK_CONSECUTIVE_FRAMES = 4

N = 7  

# Initialize screen size and scale
SCREEN_SIZE = pag.size()
DECT_SIZE = (400,400)
MOUSE_X_SCALE = 1.0
MOUSE_Y_SCALE = 1.0
SCREEN_CENTER = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)

# Scroll variables
SCROLL_SCALE = 6 # Scroll speed
SCROLL_THRESH = 0.2 # Value between 0 and 1 determining distance from center to edge of screen at which to start scrolling

# Initialize calibration vars
SCREEN_LEFT = 1
SCREEN_RIGHT = DECT_SIZE[0]
SCREEN_TOP = 1
SCREEN_BOTTOM = DECT_SIZE[1]

# Initialize the frame counters for each action as well as 
# booleans used to indicate if action is performed or not
MOUTH_COUNTER = 0
EYE_COUNTER = 0
WINK_COUNTER = 0
INPUT_MODE = True
EYE_CLICK = True
LEFT_WINK = False
RIGHT_WINK = False
SCROLL_MODE = False
CALIBRATION_MODE = False
CALIBRATION_STEP = 0
ANCHOR_POINT = (0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)

if not path.exists("bounds.pkl"):
    CALIBRATION_MODE = True

# Initialize Dlib's face detector (HOG-based) and then create
# the facial landmark predictor
shape_predictor = "model/shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Grab the indexes of the facial landmarks for the left and
# right eye, nose and mouth respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(nStart, nEnd) = face_utils.FACIAL_LANDMARKS_IDXS["nose"]
(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# Video capture
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_BUFFERSIZE, 3) 
resolution_w, resolution_h = SCREEN_SIZE

xhist = [0 for i in range(0,N-1)]
yhist = [0 for i in range(0,N-1)]

cam_w, cam_h = DECT_SIZE

unit_w = resolution_w / cam_w
unit_h = resolution_h / cam_h

#with open("data/bounds.pkl") as f:
#    MOUSE_X_SCALE, MOUSE_Y_SCALE, ANCHOR_POINT = pickle.load(f)

print("entering loop")
print(dlib.DLIB_USE_CUDA)
while 1:
    start_time = time.time()

    # Grab the frame from the threaded video file stream, resize
    # it, and convert it to grayscale
    # channels)
    _, frame = vid.read()
    frame = cv2.flip(frame, 1)
    frame = imutils.resize(frame, width=cam_w, height=cam_h)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    rects = detector(gray, 0)

    # Select first face
    if len(rects) > 0:
        rect = rects[0]
    else:
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        continue

    # Determine the facial landmarks for the face region, then
    # convert the facial landmark (x, y)-coordinates to a NumPy
    # array
    shape = predictor(gray, rect)
    shape = face_utils.shape_to_np(shape)

    # Extract the left and right eye coordinates, then use the
    # coordinates to compute the eye aspect ratio for both eyes
    mouth = shape[mStart:mEnd]
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    nose = shape[nStart:nEnd]

    # Because I flipped the frame, left is right, right is left.
    temp = leftEye
    leftEye = rightEye
    rightEye = temp

    # Average the mouth aspect ratio together for both eyes
    mar = mouth_aspect_ratio(mouth)
    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0
    diff_ear = np.abs(leftEAR - rightEAR)

    nose_point = (nose[3, 0], nose[3, 1])

    # Compute the convex hull for the left and right eye, then
    # visualize each of the eyes
    mouthHull = cv2.convexHull(mouth)
    leftEyeHull = cv2.convexHull(leftEye)
    rightEyeHull = cv2.convexHull(rightEye)
    # Check to see if the eye aspect ratio is below the blink
    # threshold, and if so, increment the blink frame counter
    if diff_ear > WINK_AR_DIFF_THRESH:

        if leftEAR < rightEAR:
            if leftEAR < EYE_AR_THRESH:
                WINK_COUNTER += 1

                if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                    pag.click(button='left')

                    WINK_COUNTER = 0

        elif leftEAR > rightEAR:
            if rightEAR < EYE_AR_THRESH:
                WINK_COUNTER += 1

                if WINK_COUNTER > WINK_CONSECUTIVE_FRAMES:
                    pag.click(button='right')

                    WINK_COUNTER = 0
        else:
            WINK_COUNTER = 0
    elif not SCROLL_MODE:
        if ear <= EYE_AR_THRESH:
            EYE_COUNTER += 1

            if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
                SCROLL_MODE = not SCROLL_MODE
                # INPUT_MODE = not INPUT_MODE
                EYE_COUNTER = 0

                # nose point to draw a bounding box around it

        else:
            EYE_COUNTER = 0
            WINK_COUNTER = 0

    if mar > MOUTH_AR_THRESH:
        MOUTH_COUNTER += 1

        if MOUTH_COUNTER >= MOUTH_AR_CONSECUTIVE_FRAMES:
            # if the alarm is not on, turn it on
            #INPUT_MODE = not INPUT_MODE
            # SCROLL_MODE = not SCROLL_MODE
            MOUTH_COUNTER = 0
            CALIBRATION_MODE = True
            INPUT_MODE = False
    else:
        MOUTH_COUNTER = 0
    if SCROLL_MODE:
        if ear >= EYE_AR_THRESH:
            EYE_COUNTER += 1

            if EYE_COUNTER > EYE_AR_CONSECUTIVE_FRAMES:
                SCROLL_MODE = not SCROLL_MODE
                # INPUT_MODE = not INPUT_MODE
                EYE_COUNTER = 0

                # nose point to draw a bounding box around it

        else:
            EYE_COUNTER = 0
    if CALIBRATION_MODE:
        cv2.putText(frame, "CALIBRATING!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
        key = cv2.waitKey(30) & 0xFF
        if CALIBRATION_STEP==0:
            CALIBRATION_STEP += 1
            key = 0xFF
            continue
        elif CALIBRATION_STEP==1:
            cv2.putText(frame, 'CENTER NOSE AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                ANCHOR_POINT = nose_point
                CALIBRATION_STEP += 1
                key = 0xFF
                continue
        elif CALIBRATION_STEP==2:
            cv2.putText(frame, 'MOVE NOSE TO FAR LEFT AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                SCREEN_LEFT = nose_point[0]
                CALIBRATION_STEP += 1
                key = 0xFF
                continue
        elif CALIBRATION_STEP==3:
            cv2.putText(frame, 'MOVE NOSE TO FAR RIGHT AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                SCREEN_RIGHT = nose_point[0]
                CALIBRATION_STEP += 1
                key = 0xFF
                continue
        elif CALIBRATION_STEP==4:
            cv2.putText(frame, 'MOVE NOSE TO TOP AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                SCREEN_TOP = nose_point[1]
                CALIBRATION_STEP += 1
                key = 0xFF
                continue
        elif CALIBRATION_STEP==5:
            cv2.putText(frame, 'MOVE NOSE TO BOTTOM AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                SCREEN_BOTTOM = nose_point[1]
                #Calculate scales
                MOUSE_X_SCALE = 1.2*DECT_SIZE[0]/(SCREEN_BOTTOM - SCREEN_TOP)
                MOUSE_Y_SCALE = 1.2*DECT_SIZE[1]/(SCREEN_RIGHT - SCREEN_LEFT)
                CALIBRATION_MODE = False
                INPUT_MODE = True
                CALIBRATION_STEP = 0

                with open("data/bounds.pkl", "wb") as f:
                    pickle.dump([MOUSE_X_SCALE, MOUSE_Y_SCALE, ANCHOR_POINT], f)

                key = 0xFF
                cv2.destroyAllWindows()

                continue
        cv2.drawContours(frame, [mouthHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(frame, [rightEyeHull], -1, YELLOW_COLOR, 1)
        cv2.line(frame, ANCHOR_POINT, nose_point, BLUE_COLOR, 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        continue


        
    if INPUT_MODE:
        mx, my = calculate_pixel_delta(SCREEN_SIZE, DECT_SIZE, nose_point, ANCHOR_POINT, (MOUSE_X_SCALE, MOUSE_Y_SCALE))
        if SCROLL_MODE:
            d = my/(SCREEN_SIZE[1] /2)
            s = scroll_calc(d, SCROLL_THRESH,-SCROLL_SCALE)
            pag.scroll(s)
        else:
            #print((mx,my))
            xhist[1:(len(xhist)-1)] = xhist[0:(len(xhist)-2)]
            xhist[0] = mx
            yhist[1:(len(yhist)-1)] = yhist[0:(len(yhist)-2)]
            yhist[0] = my
            x = int(np.mean(xhist))
            y = int(np.mean(yhist))
            
            pag.moveTo(x+SCREEN_SIZE[0]//2, y+SCREEN_SIZE[1]//2, duration=0.001)


# Do a bit of cleanup
cv2.destroyAllWindows()
vid.release()
 