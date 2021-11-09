import os
import pickle
#import time
from Xlib.X import NONE

import cv2
import dlib
import numpy as np
import pyautogui as pag
import json

from utils import *
from facedetector import *
from calibration import *
from gesturedetection import *

# Initialize Dlib's face detector (HOG-based) and then create
# the facial landmark predictor
shape_predictor = "model/shape_predictor_68_face_landmarks.dat"
face_detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)

# Grab the indexes of the facial landmarks for the left and
# right eye, nose and mouth respectively

detector = Detector(face_detector, predictor)

print("Using CUDA: "+str(dlib.DLIB_USE_CUDA))#

if os.path.isfile("data/bounds.json"):
    with open("data/bounds.json") as file:
        bounds = dotdict(json.load(file))
    control(detector, bounds) #control the computer 

while 1:
    bounds = calibrate(detector)
    control(detector, bounds) #control the computer
    break
    # Do a bit of cleanup
cv2.destroyAllWindows()
detector.release()
 