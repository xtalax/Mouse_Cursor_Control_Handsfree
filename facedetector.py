from utils import *
import cv2
from imutils import face_utils
import imutils
from pyautogui import size as screensize

DECT_SIZE = (400,400)
SCREEN_SIZE = screensize()


class Detector:
    def __init__(self, detector, predictor):
        self.detector = detector
        self.predictor = predictor
        # Video feed
        self.vid = cv2.VideoCapture(1)
        self.vid.set(cv2.CAP_PROP_BUFFERSIZE, 3) 
        self.feed_w, self.feed_h = DECT_SIZE

    def detect_faces(self):
        _, frame = self.vid.read()
        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=self.feed_w, height=self.feed_h)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face_rects = self.detector(gray, 0)
        if len(face_rects) > 0:
            face_rect = face_rects[0]
        else:
            return (None,None)

        points = self.predictor(gray, face_rect)
        return face_utils.shape_to_np(points), frame
        # Detect faces in the grayscale frame

    
        
class Face:
    def __init__(self, points, frame, memory = 6):
        self.frame = frame
        self.points = points
        self.mouth = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["mouth"])
        self.nose = rangeindex(points,face_utils.FACIAL_LANDMARKS_IDXS["nose"])
        self.rightEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["left_eye"])
        self.leftEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["right_eye"])
        self.rightBrow = rangeindex(points,(22,27))
        self.leftBrow = rangeindex(points,(17,22))
        #set face origin to nose point
        self.origin = (self.nose[3, 0], self.nose[3, 1])
        self.originhist = [self.originfactor for i in range(memory)]
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

    def update  (self, points, frame):
        self.frame = frame
        self.points = points
        self.mouth = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["mouth"])
        self.nose = rangeindex(points,face_utils.FACIAL_LANDMARKS_IDXS["nose"])
        self.rightEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["left_eye"])
        self.leftEye = rangeindex(points, face_utils.FACIAL_LANDMARKS_IDXS["right_eye"])
        self.rightBrow = rangeindex(points,(22,27))
        self.leftBrow = rangeindex(points,(17,22))
        #set face origin to nose point
        origin = (self.nose[3, 0], self.nose[3, 1])
        self.origin, self.originhist = histupdate(origin, self.originhist)
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

    
    def brow_height(self):
        lbrowdist = np.linalg.norm(np.mean(self.leftBrow)-np.mean(self.leftEye))
        rbrowdist = np.linalg.norm(np.mean(self.rightBrow)-np.mean(self.rightEye))

        browdist = (lbrowdist + rbrowdist)/2
        return browdist

    def extract_EAR(self):
        lear = eye_aspect_ratio(self.leftEye)
        rear = eye_aspect_ratio(self.rightEye)
        ear = (lear + rear) / 2.0
        diff_ear = np.abs(lear - rear)
        larea = area(self.leftEye)
        rarea = area(self.rightEye)
        return lear,rear,ear,diff_ear

    def extract_mouth_metrics(self):
        mar = mouth_aspect_ratio(self.mouth)
        sf = smile_flatness(self.mouth)
        ff = frown_flatness(self.mouth)
        marea = area(self.mouth)
        return mar,sf,ff,marea

