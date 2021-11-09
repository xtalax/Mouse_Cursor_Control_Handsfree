import pyautogui as pag
from utils import *
pag.FAILSAFE = False

# -------------------------------
# Gestures
# -------------------------------
# Define commands to run when a given gesture is detected.
# Initialise any variables that are persistent or shared between gestures in the __init__ for the class `ControlSettings` in gesture

def leftwink(face, b, s):
    pag.click(button='left')

def rightwink(face, b, s):
    pag.click(button='right')
    
def squint(face, b, s):
    x = None # Dummy command

def wideeyes(face, b, s):
    x = None # Dummy command

def restingeyes(face, b, s):
    x = None # Dummy command

def raisedbrows(face, b, s):
    x = None # Dummy command

def restingbrows(face, b, s):
    x = None # Dummy command

def smile(face, b, s):
    x = None # Dummy command

def frown(face, b, s):
    x = None # Dummy command

def omouth(face, b, s):
    x, y = (s.x, s.y)
    d = 2*(y - s.scrolldatum)/(pag.size()[1]) 
    s = scroll_scale(d, s.scrollthresh, s.scrollspeed)
    pag.scroll(s)

def widemouth(face, b, s):
    x = None # Dummy command

def pog(face, b, s):
    x = None # Dummy command

def restingmouth(face, b, s):
    x = None # Dummy command

def any(face, b, s):
    if any([np.linalg.norm(face.originhist[i]-face.origin)>s.mousethresh for i in range(1, len(face.originhist)-1)]): # only move if head hoves more than a certain threshold
    #print((mx,my))
        pag.moveRel(int(s.k*(s.x-s.xold)), int(s.k*(s.y-s.yold)), duration=0.05)
        s.xold = s.x
        s.yold = s.y