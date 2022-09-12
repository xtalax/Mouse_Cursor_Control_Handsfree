from utils import *
import pyautogui as pag   
import time

from Xlib.display import Display

class ControlSettings:
    def __init__(self, detector, face, b):

        self.display = Display()
        self.screen = self.display.screen()

        self.feed_w = detector.feed_w
        self.feed_h = detector.feed_h
        self.calibrate = False
        # scroll settings
        self.scrollthresh = 0.005
        self.scrollspeed = 6
        self.scrolldatum = pag.size()[1]//2
        self.steptime = 0.1
        self.steptimehist = [self.steptime for i in range(face.memory)]
        # mouse settings
        self.mousespeed = 1.0    
        self.stickiters = 12 # number of iterations of low motion before mouse sticks
        self.mousei = 0
        self.mousethresh = 0#20 # pinosexel delta threshold constituting low motion

        self.isclicking = False
        self.clickstarttime = time.time()
        self.clickdelay = 0.1

        self.isscrolling = False
        self.scrollstarted = False
        self.scrolltime = time.time()
        self.scrolldelay = 0.1

        self.nosex = b.center[0]
        self.nosey = b.center[1]

        self.eyex = face.eyex
        self.eyey = face.eyey

        self.mousexold = self.nosex
        self.mouseyold = self.nosey

    def update(self, face, b, elapsed):
        # Code to be run every loop with new face information

        self.nosex, self.nosey = calculate_pixel_delta(pag.size(), (self.feed_w, self.feed_h), face.origin, b.center, (b.kx, b.ky))

        self.eyex, self.eyey = calculate_pixel_delta(pag.size(), (self.feed_w, self.feed_h), (face.eyex, face.eyey), (0,0), (b.eyekx, b.eyeky))
        

        self.steptime, self.steptimehist = histupdate(elapsed, self.steptimehist)