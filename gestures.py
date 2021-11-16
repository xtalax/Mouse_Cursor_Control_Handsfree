import pyautogui as pag
from utils import *
import actions
pag.FAILSAFE = False
LOGGING = True

# -------------------------------
# Gestures
# -------------------------------
# Define commands to run when a given gesture is detected.
# Initialise any variables that are persistent or shared between gestures in the __init__ for the class `ControlSettings` in gesture

def leftwink(face, b, s):
    if LOGGING:
        print("Left Wink Detected")

    None
def rightwink(face, b, s):
    if LOGGING:
        print("Right Wink Detected")

    None
def squint(face, b, s):
    if LOGGING:
        print("Squint Detected")
    s.scrollmode = True #
    s.mousespeed = 1.0

def wideeyes(face, b, s):
    if LOGGING:
        print("Wide Eyes Detected")
    s.mousespeed = 0.5

def restingeyes(face, b, s):
    if LOGGING:
        print("Eyes Resting")
    s.mousespeed = 1.0

def raisedbrows(face, b, s):
    if LOGGING:
        print("Brows Raised")
    x = None # Dummy command

def restingbrows(face, b, s):
    if LOGGING:
        print("Brows Resting")
    x = None # Dummy command

def smile(face, b, s):
    if LOGGING:
        print("Smile Detected")
    #x = None # Dummy command

def frown(face, b, s):
    if LOGGING:
        print("Frown Detected")
    #pag.click(button='right')
    #x = None # Dummy command

def omouth(face, b, s):
    if LOGGING:
        print("O mouth Detected")



def widemouth(face, b, s):
    if LOGGING:
        print("Wide mouth Detected")

    x = None # Dummy command

def pog(face, b, s):
    if LOGGING:
        print("Pog Detected")
    #s.calibrate=True # Dummy command

def restingmouth(face, b, s):
    if LOGGING:
        print("Mouth Resting")

    x = None # Dummy command

def scrollmode(face, b, s):
    x, y = (s.nosex, s.nosey)
    d = -(y)/(pag.size()[1]) 
    s = scroll_scale(d, s.scrollthresh, s.scrollspeed)
    pag.scroll(s)

def mousemode(face, b, s):
    #print((face.eyex, face.eyey))
    actions.controlmouse(s.nosex, s.nosey, s)
    None