from utils import *
import pyautogui as pag   

class ControlSettings:
    def __init__(self, detector, face, b):
        self.feed_w = detector.feed_w
        self.feed_h = detector.feed_h
        self.scrollthresh = 0.01
        self.scrollspeed = 6
        self.scrolldatum = b.center[1]
        self.mousethresh = 2.1 # pixel delta threshold before mouse starts to move
        self.mousespeed = 1.0

        self.x = b.center[0]
        self.y = b.center[1]
        self.xold = b.center[0]
        self.yold = b.center[1]
    def update(self, face, b):
        # Code to be run every loop with new face information
        self.x, self.y = calculate_pixel_delta(pag.size(), (self.feed_w, self.feed_h), face.origin, b.center, (b.kx, b.ky))