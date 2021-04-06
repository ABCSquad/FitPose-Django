import numpy as np
import math
from body_parts import *

#Angle using arctan2
def angle(a,b,c):
    ba = a - b
    bc = c - b
    angle = math.atan2(bc[1], bc[0]) - math.atan2(ba[1], ba[0])
    if (angle < 0):
        angle += 2 * math.pi
    angle_in_deg = (angle*180)/math.pi
    return angle_in_deg
      
#Used for calculating angle between 3 specified keypoints (angles calculated clockwise wrt what is shown on the screen - laterally inverted)
def keypoint_angle(keypoints,a,b,c):
    a1 = keypoints[a]["X"]*100,keypoints[a]["Y"]*100
    b1 = keypoints[b]["X"]*100,keypoints[b]["Y"]*100
    c1 = keypoints[c]["X"]*100,keypoints[c]["Y"]*100
    a2,b2,c2 = np.array(list(a1)), np.array(list(b1)), np.array(list(c1))
    angle1 = angle(a2,b2,c2)
    return(angle1,a2,b2,c2)

#Function to scale keypoint values to frame coordinates
def keypoint_scale(image, position):
    frame_height, frame_width = image.shape[:2]
    position *= np.array([frame_width, frame_height])
    position = np.around(position, 5).flatten().astype(np.int).tolist()  
    return position

#Function to draw vector given a start keypoint and an angle wrt positive x axis
def draw_vector(image, keypoints, direction_flag, side):
    length = 150
    if side.lower() == 'right':
        p1 = (keypoints[LEFT_ELBOW]["X"],keypoints[LEFT_ELBOW]["Y"])
        if direction_flag == 1:
            draw_angle = 155
        elif direction_flag == 0:
            draw_angle = 230
    elif side.lower() == 'left':
        p1 = (keypoints[RIGHT_ELBOW]["X"],keypoints[RIGHT_ELBOW]["Y"])
        if direction_flag == 1:
            draw_angle = 25
        elif direction_flag == 0:
            draw_angle = 320
    p1 = keypoint_scale(image, p1)
    p2 =  (int(p1[0] + length* math.cos(draw_angle * (math.pi/180.0))) , int(p1[1] + (-length) * math.sin(draw_angle * (math.pi/180.0))))   

    return p1, p2

#Function maps a range a to b and returns the output for a value 's' from range a
def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
