import pyautogui as pag
import numpy as np
import time
import utils

# a function to hide the mouse cursor
def hidecursor():
    pag.mouseDown()
    pag.mouseUp()

def click(button, s):
    if not s.isclicking:
        s.isclicking = True
        s.clickstarttime = time.time()
        return
    else:
        if time.time() > s.clickstarttime + s.clickdelay: #click only after delay has elapsed
            pag.click(button=button)
            s.isclicking = False

def enablescroll(s):
    if not s.isscrolling:
        if s.scrollstarted:
            if time.time() > s.scrolltime + s.scrolldelay: #scroll only after delay has elapsed
                s.isscrolling = True
                s.scrollstarted = False
                s.scrolltime = time.time()
        else:
            s.scrollstarted = True
            s.scrolltime = time.time()
    else:
        s.scrolltime = time.time()

def scroll(y, s):
    d = -(y)/(pag.size()[1]) 
    s = utils.scroll_scale(d, s.scrollthresh, s.scrollspeed)
    pag.scroll(s)

def controlmouse(x,y,s):
    xold = s.mousexold
    yold = s.mouseyold
    if np.linalg.norm((x-xold, y-yold))<s.mousethresh: # only move if head hoves more than a certain threshold
        s.mousei +=1
    else:
        if s.mousei >= s.stickiters:
            x = xold
            y = yold
        s.mousei = 0
    if s.mousei <= s.stickiters:
        pag.moveRel(s.mousespeed*(x-xold), s.mousespeed*(y-yold), duration=s.steptime)
        s.mousexold = x
        s.mouseyold = y