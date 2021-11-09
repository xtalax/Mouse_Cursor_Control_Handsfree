from facedetector import Face
import pyautogui as pag
from utils import *
from ControlSettings import *
import gestures

def control(detector, b):

    while 1: #loop until face detected
        points, frame = detector.detect_faces()
        if points is not None:
            break
            
    face = Face(points, frame)
    settings = ControlSettings(detector, face, b)

    while 1:
        points, frame = detector.detect_faces()
        if points is None:
            continue
        face.update(points, frame)

        settings.update(face, b)

# --------------------------------
# # Gesture detection logic
# --------------------------------

        if face.diffar > b.wink:
            if face.leftar < face.rightar:
                if face.lear < b.eclosed:
                    gestures.leftwink(face, b, settings)

            elif face.leftar > face.rightar:
                if face.rear < b.eclosed:
                    gestures.rightwink(face, b, settings)

        if face.moutharea < b.resto: # if mouth round 
            gestures.omouth(face, b, settings)
        if face.moutharea > b.resto:
            if face.moutharea > b.mouthopen: # if mouth open
                gestures.mouthopen(face, b, settings)
            else:
                gestures.restingmouth(face, b, settings)
                       
        if face.eyear < b.squint:
            gestures.squint(face, b, settings)
        elif face.eyear > b.wide:
            gestures.wideeyes(face, b, settings)
        else:
            gestures.restingeyes(face, b, settings)

        if face.smilefactor > b.smile: # if smile
            gestures.smile(face, b, settings)

        if face.frownfactor > b.frown: # if frown
            gestures.frown(face, b, settings)

        if face.mar > b.pog: #if pog, calibrate
            gestures.pog(face, b, settings)

        gestures.any(face, b, settings) # commands to run every time
