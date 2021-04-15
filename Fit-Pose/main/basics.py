import numpy as np
import math
import cv2
from main.body_parts import *

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

#Function maps a range a to b and returns the output for a value 's' from range a
def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))
  
def dotted_line(img,pt1,pt2,color,thickness, gap):
    pts = [pt1, pt2] 

    s=pts[0]
    e=pts[0]
    pts.append(pts.pop(0))
    for p in pts:
        s=e
        e=p
        dist =((pt1[0]-pt2[0])**2+(pt1[1]-pt2[1])**2)**.5
        pts= []
        for i in  np.arange(0,dist,gap):
            r=i/dist
            x=int((pt1[0]*(1-r)+pt2[0]*r)+.5)
            y=int((pt1[1]*(1-r)+pt2[1]*r)+.5)
            p = (x,y)
            pts.append(p)
            for i in range(len(pts)-1):
            #cv2.circle(img,p,thickness,color,-1)
                if i%2 == 0:
                    cv2.line(img, pts[i], pts[i+1], color, thickness)



#Function to draw vector given a start keypoint and an angle wrt positive x axis
def draw_vector_bicep_curl(image, keypoints, direction_flag, side):
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

#Function to draw vector given a start keypoint and an angle wrt positive x axis
def draw_vector_ohp(image, keypoints, direction_flag, hand):
    length = 100
    
    if hand.lower() == "right":
        p1 = (keypoints[LEFT_SHOULDER]["X"],keypoints[LEFT_SHOULDER]["Y"])
        if direction_flag == 1:
            draw_angle1 = 80
            draw_angle2 = 90
        elif direction_flag == 0:
            draw_angle1 = 350
            draw_angle2 = 90
    elif hand.lower() == "left":
        p1 = (keypoints[RIGHT_SHOULDER]["X"],keypoints[RIGHT_SHOULDER]["Y"])
        if direction_flag == 1:
            draw_angle1 = 100
            draw_angle2 = 90
        elif direction_flag == 0:
            draw_angle1 = 190
            draw_angle2 = 90
    
    p1 = keypoint_scale(image, p1)
    p2 =  (int(p1[0] + length* math.cos(draw_angle1 * (math.pi/180.0))) , int(p1[1] + (-length) * math.sin(draw_angle1 * (math.pi/180.0)))) 

    q1 = p2
    if direction_flag == 1:
        q2 =  (int(q1[0] + length* math.cos((draw_angle2) * (math.pi/180.0))) , int(q1[1] + (-length) * math.sin((draw_angle2) * (math.pi/180.0)))) 
    if direction_flag == 0:
        q2 =  (int(q1[0] + length* math.cos((draw_angle2) * (math.pi/180.0))) , int(q1[1] + (-length) * math.sin((draw_angle2) * (math.pi/180.0))))

    return p1, p2, q1, q2

def draw_vector_lateral(image, keypoints, direction_flag, hand):
    length = 100
    
    if hand.lower() == "right":
        p1 = (keypoints[LEFT_SHOULDER]["X"],keypoints[LEFT_SHOULDER]["Y"])
        if direction_flag == 1:
            draw_angle1 = 10
            draw_angle2 = 12
        elif direction_flag == 0:
            draw_angle1 = 280
            draw_angle2 = 275
    elif hand.lower() == "left":
        p1 = (keypoints[RIGHT_SHOULDER]["X"],keypoints[RIGHT_SHOULDER]["Y"])
        if direction_flag == 1:
            draw_angle1 = 170
            draw_angle2 = 168
        elif direction_flag == 0:
            draw_angle1 = 260
            draw_angle2 = 265
    
    p1 = keypoint_scale(image, p1)
    p2 =  (int(p1[0] + length* math.cos(draw_angle1 * (math.pi/180.0))) , int(p1[1] + (-length) * math.sin(draw_angle1 * (math.pi/180.0)))) 

    q1 = p2
    if direction_flag == 1:
        q2 =  (int(q1[0] + length* math.cos((draw_angle2) * (math.pi/180.0))) , int(q1[1] + (-length) * math.sin((draw_angle2) * (math.pi/180.0)))) 
    if direction_flag == 0:
        q2 =  (int(q1[0] + length* math.cos((draw_angle2) * (math.pi/180.0))) , int(q1[1] + (-length) * math.sin((draw_angle2) * (math.pi/180.0))))

    return p1, p2, q1, q2

def initialize_stats(stats_dict):
    stats_dict['right_shoulder_angle'] = -1
    stats_dict['right_elbow_angle'] = -1
    stats_dict['left_shoulder_angle'] = -1
    stats_dict['left_elbow_angle'] = -1
    stats_dict['hip_angle'] = -1
    stats_dict['arm_right_deviation'] = -1
    stats_dict['arm_left_deviation'] = -1
    stats_dict['hip_deviation'] = -1

def initialize_messages(messages):
    messages["msg1"] = ""
    messages["msg2"] = ""
    messages["msg3"] = ""
    messages["msg4"] = ""
    # messages["msg5"] = ""
    # messages["msg6"] = ""
