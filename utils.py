import numpy as np
from math import exp
import json
import inspect

def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def show(x):
    return print(retrieve_name(x)[0]+": "+str(x))

def rangeindex(v, idx):
    return v[idx[0]:idx[1]]

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    
def histupdate(x, hist):
    hist[1:] = hist[:(len(hist)-2)]
    hist[0] = x
    return (np.mean(hist), hist)

# Returns EAR given eye landmarks
def eye_aspect_ratio(eye):
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
def area(pts):
    lines = np.hstack([pts,np.roll(pts,-1,axis=0)])
    area = 0.5*abs(sum(x1*y2-x2*y1 for x1,y1,x2,y2 in lines))
    return area


# Returns MAR given eye landmarks
def mouth_aspect_ratio(mouth):
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

def smile_flatness(mouth):
        # Compute mouth upper line flatness
    a = mouth[3] - mouth[0]
    b = mouth[6] - mouth[0]
    return np.dot(a/np.linalg.norm(a), b/np.linalg.norm(b))

def frown_flatness(mouth):
        # Compute mouth lower line flatness
    a = mouth[9] - mouth[0]
    b = mouth[6] - mouth[0]
    return np.dot(a/np.linalg.norm(a), b/np.linalg.norm(b))


def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]


# Take in nose position and calculate output mouse position as a function of the scale factor and screen size
def calculate_pixel_delta(screen,dect,nosepos,anchorpoint,scale):
    sx, sy = screen
    dx, dy = dect #detection res
    nx, ny = nosepos
    cx, cy = anchorpoint #center point
    kx, ky = scale #xy scale factor

    x, y = (int(sx*kx*(nx-cx)/dx), int(sy*ky*(ny-cy)/dy))

    return (x,y)


def scroll_scale(d, thresh, scale): 
    if d > 0:
        if d > thresh:
            d -= thresh
        else:
            d = 0.0
        d = d**2
    else:
        if d < -thresh:
            d+=thresh
        else:
            d = 0.0 
        d = -d**2
    return int(d*scale) 

def look_scale(d, mid, thresh, scale): 
    d=d-mid
    if d > 0:
        if d > thresh-mid:
            d -= thresh-mid
            d = exp(-d/(scale-mid)) 
        else:
            d = 1.0
    else:
        if d < -thresh-mid:
            d+=thresh-mid
            d = 1.0-d/(scale-mid)
        else:
            d = 1.0
    return d

def thresh_scale(a,b,x):
    return (a*x + (1-x)*b) / 2

# Return direction given the nose and anchor points.
def direction(nose_point, anchor_point, w, h, multiple=1):
    nx, ny = nose_point
    x, y = anchor_point

    if nx > x + multiple * w:
        return 'right'
    elif nx < x - multiple * w:
        return 'left'

    if ny > y + multiple * h:
        return 'down'
    elif ny < y - multiple * h:
        return 'up'

    return '-'
