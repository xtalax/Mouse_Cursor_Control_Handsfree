from facedetector import Face
from utils import *
import pyautogui as pag
pag.FAILSAFE = False

def control(detector, b):
    scrollframes = 4
    winkframes = 3
    calibrationframes = 8
    scrollthresh = 0.05
    N = 6
    iscroll = 0
    iwink = 0
    icalibration = 0
    scrollmode=False
    scrolldatum = b.center[1]

    xhist = [0.0 for i in range(0,N-1)]
    yhist = [0.0 for i in range(0,N-1)]
    khist = [0.0 for i in range(0,N-1)]
    screen = pag.size()
    xold = screen[0]//2
    yold = screen[1]//2

    while 1:
        points, frame = detector.detect_faces()
        if points is None:
            continue
        
        face = Face(points, frame)

        if face.diffear > b.wink:

            if face.lear < face.rear:
                if face.lear < b.eclosed:
                    iwink += 1

                    if iwink > winkframes:
                        pag.click(button='left')

                        iwink = 0

            elif face.lear > face.rear:
                if face.rear < b.eclosed:
                    iwink += 1

                    if iwink > winkframes:
                        pag.click(button='right')

                        iwink = 0
        else:
            iwink = 0

        if scrollmode:
            if face.mar < b.tiny: # if mouth round
                iscroll += 1

                if iscroll > scrollframes:
                    scrollmode = not scrollmode
                    # INPUT_MODE = not INPUT_MODE
                    scrolldatum = face.origin[1]
                    iscroll = 0

                    # nose point to draw a bounding box around it

            else:
                iscroll = 0
        else:
            if face.mar > b.tiny:
                iscroll += 1

                if iscroll > scrollframes:
                    scrollmode = not scrollmode
                    # INPUT_MODE = not INPUT_MODE
                    iscroll = 0
            else:
                iscroll = 0

        if face.mar > b.pog: #if pog, calibrate
            icalibration += 1

            if icalibration >= calibrationframes:
                icalibration = 0
                return None
        else:
            icalibration = 0
        
        if face.ear < b.squint:
            mk = 0.3
        elif face.ear > b.wide:
            mk = 1.2
        else:
            mk = 1.0

    # print("k: "+str(k))
        scalex = b.kx
        scaley = b.ky
        mx, my = calculate_pixel_delta(pag.size(), (detector.feed_w, detector.feed_h), face.origin, b.center, (scalex, scaley))

        xhist[1:(len(xhist)-1)] = xhist[0:(len(xhist)-2)]
        xhist[0] = mx
        yhist[1:(len(yhist)-1)] = yhist[0:(len(yhist)-2)]
        yhist[0] = my
        khist[1:(len(khist)-1)] = khist[0:(len(khist)-2)]
        khist[0] = mk
        k = np.mean(khist)
        print(k)

        x = np.mean(xhist)
        y = np.mean(yhist)
        
        if scrollmode:
            d = 2*(y - scrolldatum)/(pag.size()[1])
            s = scroll_scale(d, scrollthresh, -6)
            pag.scroll(s)
        else:
            #print((mx,my))

            pag.moveRel(int(k*(x-xold)), int(k*(y-yold)), duration=0.075)
            xold = x
            yold = y