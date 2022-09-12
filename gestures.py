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
    s.isscrolling = True #

def wideeyes(face, b, s):
    if LOGGING:
        print("Wide Eyes Detected")

def restingeyes(face, b, s):
    if LOGGING:
        print("Eyes Resting")
    s.mousespeed = 1.0

def raisedbrows(face, b, s):
    if LOGGING:
        print("Brows Raised")
    s.mousespeed = 0.5
    x = None # Dummy command

def restingbrows(face, b, s):
    if LOGGING:
        print("Brows Resting")
    s.mousespeed = 1.0
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

def mouthopen(face, b, s):
    None

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

def isscrolling(face, b, s):
    actions.scroll(s.nosey, s)

def mousemode(face, b, s):
    #print((face.eyex, face.eyey))
    actions.controlmouse(s.nosex, s.nosey, s)
