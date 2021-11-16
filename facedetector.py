from utils import *
import cv2
from imutils import face_utils
from gaze_tracking import GazeTracking
from statistics import mean
from pyautogui import size as screensize

DECT_SIZE = (640,480)
SCREEN_SIZE = screensize()


class Detector:
    def __init__(self, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        # Video feed
        for i in range(0,6): #scan for video feed
            self.vid = cv2.VideoCapture(i)
            self.vid.set(3, DECT_SIZE[0])
            self.vid.set(4, DECT_SIZE[1])
            frame = self.vid.read()
            if frame is not None:
                break
            if i == 6:
                raise RuntimeError("Video feed not found.")
        
        self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 3) 
        self.feed_w, self.feed_h = DECT_SIZE

    def detect_faces(self):
        _, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_rects = self.detector(gray, 0)
        if len(face_rects) > 0:
            face_rect = face_rects[0]
        else:
            return (None,None)

        points = self.predictor(gray, face_rect)
        return points, frame
        # Detect faces in the grayscale frame

    
        
class Face:
    def __init__(self, landmarks, frame, memory = 5):

        self.frame = frame
        self.gaze = GazeTracking()
        self.gazecalibrated = False

        points = face_utils.shape_to_np(landmarks)
        self.memory = memory
        self.mouth = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["mouth"])
        self.nose = rangeindex(points,face_utils.FACIAL_LANDMARKS_IDXS["nose"])
        self.rightEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["left_eye"])
        self.leftEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["right_eye"])
        self.rightBrow = rangeindex(points,(22,27))
        self.leftBrow = rangeindex(points,(17,22))
        #set face origin to nose point
        print(face_utils.FACIAL_LANDMARKS_IDXS["left_eye"])
        nosex = np.mean([n[0] for n in self.nose])
        nosey = np.mean([n[1] for n in self.nose])

        self.origin = (nosex, nosey)
        self.originhistx = [self.origin[0] for i in range(memory)]
        self.originhisty = [self.origin[1] for i in range(memory)]

        # Gaze init
        self.gaze.refresh(frame, landmarks)

        self.eyex = None
        self.eyey = None

        self.eyexhist = [self.eyex for i in range(memory)]
        self.eyeyhist = [self.eyey for i in range(memory)]

        # Mouth aspect ratio, smile factor (upper mouth flatness), frown factor (lower mouth flatness), mouth area
        self.mar, self.smilefactor, self.frownfactor, self.moutharea = self.extract_mouth_metrics()

        self.marhist = [self.mar for i in range(memory)]
        self.smilefactorhist = [self.smilefactor for i in range(memory)]
        self.frownfactorhist = [self.frownfactor for i in range(memory)]
        self.mouthareahist = [self.moutharea for i in range(memory)]
        #extract metrics from the points

        # left, right eye aspect ratio, average aspect ratio, differential aspect ratio
        self.leftar, self.rightar, self.eyear, self.diffar = self.extract_EAR()
        self.leftarhist = [self.leftar for i in range(memory)]
        self.rightarhist = [self.rightar for i in range(memory)]
        self.eyearhist = [self.eyear for i in range(memory)]
        self.diffarhist = [self.diffar for i in range(memory)]
        # brow height
        self.browdist = self.brow_height()
        self.browdisthist = [self.browdist for i in range(memory)]

    def update(self, landmarks, frame):
        self.frame = frame
        points = face_utils.shape_to_np(landmarks)
        self.gaze.refresh(frame, landmarks)

        self.outline = rangeindex(points, (0, 26))
        self.mouth = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["mouth"])
        self.nose = rangeindex(points,face_utils.FACIAL_LANDMARKS_IDXS["nose"])
        self.rightEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["left_eye"])
        self.leftEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["right_eye"])
        self.rightBrow = rangeindex(points,(22,27))
        self.leftBrow = rangeindex(points,(17,22))
        #set face origin to nose point
        nosex = np.mean([n[0] for n in self.nose])
        nosey = np.mean([n[1] for n in self.nose])

        originx, self.originhistx = histupdate(nosex, self.originhistx)
        originy, self.originhisty = histupdate(nosey, self.originhisty)
        self.origin = (originx, originy)

        self.eye_update() #sets eye displacement in pixels
        # Mouth aspect ratio, smile factor (upper mouth flatness), frown factor (lower mouth flatness), mouth area
        mar, smilefactor, frownfactor, moutharea = self.extract_mouth_metrics()

        self.mar, self.marhist = histupdate(mar, self.marhist)
        self.smilefactor, self.smilefactorhist = histupdate(smilefactor, self.smilefactorhist)
        self.frownfactor, self.frownfactorhist = histupdate(frownfactor, self.frownfactorhist)
        self.moutharea, self.mouthareahist = histupdate(moutharea, self.mouthareahist)

        # left, right eye aspect ratio, average aspect ratio, differential aspect ratio
        leftar, rightar, eyear, diffar = self.extract_EAR()
        self.leftar, self.leftarhist = histupdate(leftar, self.leftarhist)
        self.rightar, self.rightarhist = histupdate(rightar, self.rightarhist)
        self.eyear, self.eyearhist = histupdate(eyear, self.eyearhist)
        self.diffar, self.diffarhist = histupdate(diffar, self.diffarhist)

        # brow height
        browdist = self.brow_height()
        self.browdist, self.browdisthist = histupdate(browdist, self.browdisthist)

    def eye_update(self):
        # Gaze update
        if self.gaze.pupils_located:
            if not self.gazecalibrated:
                if self.gaze.calibration.is_complete():
                    eyel = self.gaze.pupil_left_coords()
                    eyer = self.gaze.pupil_right_coords()
                    self.eyex = mean([eyel[0], eyer[0]]) - self.origin[0]
                    self.eyey = mean([eyel[1], eyer[1]]) - self.origin[1]

                    self.eyexhist = vechistupdate(self.eyex, self.eyexhist)
                    self.eyeyhist = vechistupdate(self.eyey, self.eyeyhist)
                    if not any(v is None for v in self.eyeyhist):
                        self.gazecalibrated = True
            else:
                eyel = self.gaze.pupil_left_coords()
                eyer = self.gaze.pupil_right_coords()
                eyex = mean([eyel[0], eyer[0]]) - self.origin[0]
                eyey = mean([eyel[1], eyer[1]]) - self.origin[1]

                self.eyex, self.eyexhist = histupdate(eyex, self.eyexhist)
                self.eyey, self.eyeyhist = histupdate(eyey, self.eyeyhist)

    
    def brow_height(self):
        lbrowdist = np.linalg.norm(np.mean(self.leftBrow)-np.mean(self.leftEye))
        rbrowdist = np.linalg.norm(np.mean(self.rightBrow)-np.mean(self.rightEye))

        browdist = (lbrowdist + rbrowdist)/2
        return browdist

    def extract_EAR(self):
        lear = self.eye_aspect_ratio(self.leftEye)
        rear = self.eye_aspect_ratio(self.rightEye)
        ear = (lear + rear) / 2.0
        diff_ear = np.abs(lear - rear)
        larea = self.area(self.leftEye)
        rarea = self.area(self.rightEye)
        return lear,rear,ear,diff_ear

    def extract_mouth_metrics(self):
        mar = self.mouth_aspect_ratio(self.mouth)
        sf = self.smile_flatness(self.mouth)
        ff = self.frown_flatness(self.mouth)
        marea = self.area(self.mouth)
        return mar,sf,ff,marea

    
    # Returns EAR given eye landmarks
    def eye_aspect_ratio(self, eye):
        # Compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        A = np.linalg.norm(eye[1] - eye[5])
        B = np.linalg.norm(eye[2] - eye[4])

        # Compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        C = np.linalg.norm(eye[0] - eye[3])

        # Compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # Return the eye aspect ratio
        return ear

    #Get area hull
    def area(self, pts):
        lines = np.hstack([pts,np.roll(pts,-1,axis=0)])
        area = 0.5*abs(sum(x1*y2-x2*y1 for x1,y1,x2,y2 in lines))
        return area


    # Returns MAR given eye landmarks
    def mouth_aspect_ratio(self, mouth):
        # Compute the euclidean distances between the three sets
        # of vertical mouth landmarks (x, y)-coordinates
        A = np.linalg.norm(mouth[2] - mouth[9])
        B = np.linalg.norm(mouth[3] - mouth[7])

        # Compute the euclidean distance between the horizontal
        # mouth landmarks (x, y)-coordinates
        D = np.linalg.norm(mouth[12] - mouth[16])

        # Compute the mouth aspect ratio
        mar = (A + B) / (2 * D)

        # Return the mouth aspect ratio
        return mar

    def smile_flatness(self, mouth):
            # Compute mouth upper line flatness
        a = mouth[3] - mouth[0]
        b = mouth[6] - mouth[0]
        return np.dot(a/np.linalg.norm(a), b/np.linalg.norm(b))

    def frown_flatness(self, mouth):
            # Compute mouth lower line flatness
        a = mouth[9] - mouth[0]
        b = mouth[6] - mouth[0]
        return np.dot(a/np.linalg.norm(a), b/np.linalg.norm(b))



