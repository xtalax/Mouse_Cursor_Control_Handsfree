import cv2
from statistics import mean
from facedetector import Face
from numpy import abs
import json
from json import JSONEncoder
from ControlSettings import ControlSettings

WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)

# TODO: 1. Average state values over multiple directions, correct thresholds as a function of nose position
# TODO: 2. 

def calibrate(detector):
    step = 0
    center = (1,1)
    while 1: #loop until face detected
        points, frame = detector.detect_faces()
        if points is not None:
            break
            
    face = Face(points, frame)
    while step<10:
        points, frame = detector.detect_faces()
        if points is None:
            continue
        
        face.update(points, frame)

        cv2.putText(face.frame, "CALIBRATING!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
        
        mouthHull = cv2.convexHull(face.mouth)
        leftEyeHull = cv2.convexHull(face.leftEye)
        rightEyeHull = cv2.convexHull(face.rightEye)
        key = cv2.waitKey(30) & 0xFF
        if step==0:
            step += 1
            key = 0xFF
        elif step==1:
            cv2.putText(face.frame, 'CENTER NOSE, O MOUTH AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                center = face.origin
                restingbrowdist = face.browdist
                minarea = face.moutharea
                tinyMAR = face.mar
                step += 1
                key = 0xFF
        elif step==2:
            cv2.putText(face.frame, 'MOVE NOSE TO FAR LEFT AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                noseleft = face.origin[0]
                step += 1
                key = 0xFF
        elif step==3:
            cv2.putText(face.frame, 'MOVE NOSE TO FAR RIGHT AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                noseright = face.origin[0]
                step += 1
                key = 0xFF
        elif step==4:
            cv2.putText(face.frame, 'MOVE NOSE TO TOP, POG AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key == 32:
                pogMAR = face.mar
                nosetop = face.origin[1]
                step += 1
                key = 0xFF
        elif step==5:
            cv2.putText(face.frame, 'MOVE NOSE TO BOTTOM, WIDE EYES', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            cv2.putText(face.frame, 'REST MOUTH AND PRESS SPACE', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

            if key == 32:
                nosebottom = face.origin[1]
                wideEAR = face.eyear
                restingMAR = face.mar
                restingff = face.frownfactor
                restingarea = face.moutharea
                #Calculate scales
                step += 1
                key = 0xFF
        elif step==6:
            cv2.putText(face.frame, 'PUT EYES IN RESTING POSTITION,', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            cv2.putText(face.frame, 'OPEN MOUTH WIDE, RAISE BROWS', (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            cv2.putText(face.frame, 'AND PRESS SPACE', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)

            if key==32:
                maxMAR = face.mar
                maxarea = face.moutharea
                opensf = face.smilefactor
                restingEAR = face.eyear
                raisedbrowdist = face.browdist
                step += 1
                key = 0xFF
        elif step==7:
            cv2.putText(face.frame, 'SQUINT EYES, SMILE AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key==32:#
                squintEAR = face.eyear
                smileMAR = face.mar
                smilesf = face.smilefactor
                step += 1 
                key = 0xFF
        elif step==8:
            cv2.putText(face.frame, 'CLOSE EYES, FROWN AND PRESS SPACE', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, RED_COLOR, 2)
            if key==32:
                closedEAR = face.eyear
                frownff = face.frownfactor
                step += 1 

                key = 0xFF

        elif step==9:
            
            bounds = Bounds(center, detector, minarea, tinyMAR, noseleft, noseright, pogMAR, nosetop, nosebottom, wideEAR, restingMAR, restingarea, maxarea, opensf, restingEAR, squintEAR, smilesf, restingff,frownff,closedEAR, raisedbrowdist, restingbrowdist)
            
            # with open("data/bounds.pkl", "wb") as f:
            #     pickle.dump([MOUSE_X_SCALE, MOUSE_Y_SCALE, ANCHOR_POINT], f)

            key = 0xFF
            cv2.destroyAllWindows()
            break

        cv2.drawContours(face.frame, [mouthHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(face.frame, [leftEyeHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(face.frame, [rightEyeHull], -1, YELLOW_COLOR, 1)
        cv2.drawContours(face.frame, [face.leftBrow], -1, YELLOW_COLOR, 1)
        cv2.drawContours(face.frame, [face.rightBrow], -1, YELLOW_COLOR, 1)

        for item in face.nose:
            cv2.drawMarker(frame, (item[0], item[1]), GREEN_COLOR, markerType=cv2.MARKER_STAR, markerSize=40, thickness=2, line_type=cv2.LINE_AA)


        cv2.line(face.frame, center, face.origin, BLUE_COLOR, 2)
        cv2.imshow("Frame", face.frame)
    
    with open('data/bounds.json', 'w') as file:
        file.write(json.dumps(bounds, indent=4, cls=EncodeBounds))
    return bounds

class Bounds:
    def __init__(self, center, detector, minarea, tinyMAR, noseleft, noseright, pogMAR, nosetop, nosebottom, wideEAR, restingMAR, restingarea, maxarea, opensf, restingEAR, squintEAR, smilesf, restingff,frownff, closedEAR, raisedbrowdist, restingbrowdist):
        self.center = [x.item() for x in center] # nose positiion when centerd
        self.kx = 1.2*detector.feed_w/(nosebottom - nosetop).item()
        self.ky=1.2*detector.feed_h/(noseright - noseleft).item() # scaling to achieve a screen width of movement with full head range
        self.mouthopen = mean([restingarea, maxarea]).item() #area threshold between resting and open
        self.tiny = mean([restingMAR, tinyMAR]).item() # aspect ratio threshold between resting and tiny
        self.resto = mean([restingarea, minarea]).item() # area threshold between resting and o mouth
        self.pog = mean([tinyMAR, pogMAR]).item() # aspect ratio threshold between o mouth and pog
        self.smile = mean([opensf, smilesf]).item() # threshold of mouth top flatness to detect smile
        self.frown = mean([restingff, frownff]).item() # threshold of mouth

        self.squint = mean([restingEAR, squintEAR]).item() # threshold to detect squint
        self.eclosed = mean([squintEAR, closedEAR]).item() # threshold to detect closed eyes

        self.wide = mean([restingEAR, wideEAR]).item() # threshold to detect wide eyes

        self.wink = mean([0.0, abs(restingEAR -closedEAR)]).item() # threshold of difference in eye aspect ratio to detect wink
        self.browraised = mean([raisedbrowdist, restingbrowdist]).item() #threshold to detect raised eyebrows 
class EncodeBounds(JSONEncoder):
    def default(self, o):
        return o.__dict__