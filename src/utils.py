import numpy as np


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


# Returns MAR given eye landmarks
def mouth_aspect_ratio(mouth):
    # Compute the euclidean distances between the three sets
    # of vertical mouth landmarks (x, y)-coordinates
    A = np.linalg.norm(mouth[13] - mouth[19])
    B = np.linalg.norm(mouth[14] - mouth[18])
    C = np.linalg.norm(mouth[15] - mouth[17])

    # Compute the euclidean distance between the horizontal
    # mouth landmarks (x, y)-coordinates
    D = np.linalg.norm(mouth[12] - mouth[16])

    # Compute the mouth aspect ratio
    mar = (A + B + C) / (2 * D)

    # Return the mouth aspect ratio
    return mar

# Take in nose position and calculate output mouse position as a function of the scale factor and screen size
def calculate_pixel_delta(screen,dect,nosepos,anchorpoint,scale):
    sx, sy = screen
    dx, dy = dect #detection res
    nx, ny = nosepos
    cx, cy = anchorpoint #center point
    kx, ky = scale #xy scale factor

    x, y = (int(sx*kx*(nx-cx)/dx), int(sy*ky*(ny-cy)/dy))

    if x<=(-screen[0]//2):
        x=(-screen[0]//2)+1
    elif x>(screen[0]//2):
        x = (screen[0]//2)

    if y<=(-screen[1]//2):
        y=(-screen[1]//2)+1
    elif y>(screen[1]//2):
        y = (screen[1]//2)
    return (x,y)

def scroll_calc(d, thresh, scale): 
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
