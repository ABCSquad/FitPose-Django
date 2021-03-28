import numpy as np
import math
import cv2
from basics import *


NOSE = 0
LEFT_EYE_INNER = 1
LEFT_EYE = 2
LEFT_EYE_OUTER = 3
RIGHT_EYE_INNER = 4
RIGHT_EYE = 5
RIGHT_EYE_OUTER = 6
LEFT_EAR = 7
RIGHT_EAR = 8
MOUTH_LEFT = 9
MOUTH_RIGHT = 10
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_ELBOW = 13
RIGHT_ELBOW = 14
LEFT_WRIST = 15
RIGHT_WRIST = 16
LEFT_PINKY = 17
RIGHT_PINKY = 18
LEFT_INDEX = 19
RIGHT_INDEX = 20
LEFT_THUMB = 21
RIGHT_THUMB = 22
LEFT_HIP = 23
RIGHT_HIP = 24
LEFT_KNEE = 25
RIGHT_KNEE = 26
LEFT_ANKLE = 27
RIGHT_ANKLE = 28
LEFT_HEEL = 29
RIGHT_HEEL = 30
LEFT_FOOT_INDEX = 31
RIGHT_FOOT_INDEX = 32

#Global flag declarations 
flag_wrong = 0
flag_right = 0
flag_right_left = 0
flag_wrong_left = 0

def shoulder_press(keypoints):
    global flag_wrong
    global flag_right
    global flag_right_left 
    global flag_wrong_left

    #Right hand angle and deviation calculation
    right_shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
    right_elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
    right_deviation = abs(right_shoulder_angle - right_elbow_angle)

    #Left hand angle and deviation calculation
    left_shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_HIP, RIGHT_SHOULDER, RIGHT_ELBOW)
    left_elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_WRIST, RIGHT_ELBOW, RIGHT_SHOULDER)
    left_deviation = abs(left_shoulder_angle - left_elbow_angle)

    #Blank white image to display stats
    stats = cv2.imread('white2.jpg') 

    stats = cv2.putText(stats, 'Stats', (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    stats = cv2.putText(stats, 'Angle at right shoulder : '+ str(round(right_shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, 'Angle at right elbow : '+ str(round(right_elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    #Evaluating the posture for the right hand using a function
    right_deviation, flag_right, flag_wrong, stats = ohp_posture_right(right_deviation, flag_right, flag_wrong, stats)
    
    stats = cv2.putText(stats, 'Angle at left shoulder : '+ str(round(left_shoulder_angle,2)), (5,115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, 'Angle at left elbow : '+ str(round(left_elbow_angle,2)), (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 
   
    #Evaluating the posture for the left hand using a function
    left_deviation, flag_right_left, flag_wrong_left, stats = ohp_posture_left(left_deviation, flag_right_left, flag_wrong_left, stats)

    return(right_shoulder_angle, right_elbow_angle, right_deviation, left_shoulder_angle, left_elbow_angle, left_deviation, stats)
    
