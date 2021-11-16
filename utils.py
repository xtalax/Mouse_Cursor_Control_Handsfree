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
    
def vechistupdate(x, hist):
    hist[1:] = hist[:(len(hist)-1)]
    hist[0] = x
    return hist

def histupdate(x, hist):
    hist = vechistupdate(x, hist)
    return (np.mean(hist), hist)

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

    x, y = sx*kx*(nx-cx)/dx, sy*ky*(ny-cy)/dy

    return (x,y)


def scroll_scale(d, thresh, scale): 
    if d > 0:
        if d > thresh:
            d -= thresh
        else:
            d = 0.0
    else:
        if d < -thresh:
            d+=thresh
        else:
            d = 0.0 
    return d*scale

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
    return (a*x + (1-x)*b)

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
