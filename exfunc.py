import numpy as np
import math
import cv2
from basics import *
from rep_counter import *
from body_parts import *
from posture_basics import *


#Global flag declarations 
flag_wrong = 0
flag_right = 0
flag_right_left = 0
flag_wrong_left = 0
direction_flag = -1

def shoulder_press(image, keypoints, reps):
    global flag_wrong
    global flag_right
    global flag_right_left 
    global flag_wrong_left
    global direction_flag

    #Right hand angle and deviation calculation
    right_shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
    right_elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
    right_deviation = abs(right_shoulder_angle - right_elbow_angle)

    #Left hand angle and deviation calculation
    left_shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_HIP, RIGHT_SHOULDER, RIGHT_ELBOW)
    left_elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_WRIST, RIGHT_ELBOW, RIGHT_SHOULDER)
    left_deviation = abs(left_shoulder_angle - left_elbow_angle)

    #Rep counter
    reps = ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps)


    #Blank white image to display stats
    stats = cv2.imread("white2.jpg") 

    stats = cv2.putText(stats, "Stats", (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    stats = cv2.putText(stats, "Angle at right shoulder : "+ str(round(right_shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at right elbow : "+ str(round(right_elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    #Evaluating the posture for the right hand using a function
    stats, flag_right, flag_wrong = ohp_posture_right(right_deviation, flag_right, flag_wrong, stats)

    #Condition to draw target vectors according to the hand motion direction 
    if reps['flag'] == 1:
      p1, p2, q1, q2 = draw_vector_ohp(image, keypoints, reps["flag"], "right")
      value = maprange((90, 0), (0, 255), 170 - right_elbow_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)
    if reps['flag'] == 0:
      p1, p2, q1, q2 = draw_vector_ohp(image, keypoints, reps["flag"], "right")
      value = maprange((0, 90), (0, 255), 170 - right_elbow_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)
    
    stats = cv2.putText(stats, "Angle at left shoulder : "+ str(round(left_shoulder_angle,2)), (5,115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at left elbow : "+ str(round(left_elbow_angle,2)), (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 
   
    #Evaluating the posture for the left hand using a function
    stats, flag_right_left, flag_wrong_left = ohp_posture_left(left_deviation, flag_right_left, flag_wrong_left, stats)

    #Condition to draw target vectors according to the hand motion direction 
    if reps['flag'] == 1:
      p1, p2, q1, q2 = draw_vector_ohp(image, keypoints, reps["flag"], "left")
      value = maprange((90, 0), (0, 255), 170 - left_elbow_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)
    if reps['flag'] == 0:
      p1, p2, q1, q2 = draw_vector_ohp(image, keypoints, reps["flag"], "left")
      value = maprange((0, 90), (0, 255), 170 - left_elbow_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)

    return(image, stats, reps)
    
def bicep_curl(image, keypoints, side, reps):
    global direction_flag

    #Right hand angles calculation
    if side.lower() == "right":
      shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_HIP, LEFT_SHOULDER, LEFT_ELBOW)
      elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_WRIST, LEFT_ELBOW, LEFT_SHOULDER)
    elif side.lower() == "left":
      shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP)
      elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)

    #Rep counter
    reps = curl_reps(shoulder_angle, elbow_angle, reps)

    #Blank white image to display stats
    stats = cv2.imread("white2.jpg") 

    stats = cv2.putText(stats, "Stats", (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    stats = cv2.putText(stats, "Angle at "+ side +" shoulder: "+ str(round(shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at "+ side +" elbow: "+ str(round(elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    #Evaluating the posture for the right hand using a function
    image, stats, direction_flag = curl_posture(image, keypoints, side, shoulder_angle, elbow_angle, stats, direction_flag)

    #Condition to draw target vectors according to the hand motion direction
    if direction_flag == 1:
        p1, p2 = draw_vector_bicep_curl(image, keypoints, direction_flag, side)
        value = maprange((95, 0), (0, 255), elbow_angle-65)
        yellow = 255 - value
        green = 0 + value
        dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
    elif direction_flag == 0:
        p1, p2 = draw_vector_bicep_curl(image, keypoints, direction_flag, side)
        value = maprange((0, 95), (0, 255), elbow_angle-65)
        yellow = 255 - value
        green = 0 + value
        dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
    
    return(image, stats, reps)

def tricep_extension(keypoints, side):
    #Right hand angles calculation
    if side.lower() == "right":
      shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_HIP, LEFT_SHOULDER, LEFT_ELBOW)
      elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_WRIST, LEFT_ELBOW, LEFT_SHOULDER)
    elif side.lower() == "left":
      shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP)
      elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)

    #Rep counter
    #reps, rep_flag = curl_reps(shoulder_angle, elbow_angle, reps, rep_flag)

    #Blank white image to display stats
    stats = cv2.imread("white2.jpg") 

    stats = cv2.putText(stats, "Stats", (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    stats = cv2.putText(stats, "Angle at "+ side +" shoulder: "+ str(round(shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at "+ side +" elbow: "+ str(round(elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    #Evaluating the posture for the right hand using a function
    stats = tricep_extension_posture(shoulder_angle, elbow_angle, stats)

    return(stats)

def lateral_raise(image, keypoints, reps):
    global flag_wrong
    global flag_right
    global flag_right_left 
    global flag_wrong_left
    global direction_flag

    #Right hand angle and deviation calculation
    right_shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
    right_elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
    right_deviation = abs(175 - right_elbow_angle)

    #Left hand angle and deviation calculation
    left_shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_HIP, RIGHT_SHOULDER, RIGHT_ELBOW)
    left_elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_WRIST, RIGHT_ELBOW, RIGHT_SHOULDER)
    left_deviation = abs(175 - left_elbow_angle)

    #Rep counter
    reps = lateral_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps)


    #Blank white image to display stats
    stats = cv2.imread("white2.jpg") 

    stats = cv2.putText(stats, "Stats", (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    stats = cv2.putText(stats, "Angle at right shoulder : "+ str(round(right_shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at right elbow : "+ str(round(right_elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    #Evaluating the posture for the right hand using a function
    stats, flag_right, flag_wrong = lateral_posture_right(right_deviation, flag_right, flag_wrong, stats)

    #Condition to draw target vectors according to the hand motion direction 
    if reps['flag'] == 1:
      p1, p2, q1, q2 = draw_vector_lateral(image, keypoints, reps["flag"], "right")
      value = maprange((0, 110), (0, 255), right_shoulder_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)
    if reps['flag'] == 0:
      p1, p2, q1, q2 = draw_vector_lateral(image, keypoints, reps["flag"], "right")
      value = maprange((110, 0), (0, 255), right_shoulder_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)
    
    stats = cv2.putText(stats, "Angle at left shoulder : "+ str(round(left_shoulder_angle,2)), (5,115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at left elbow : "+ str(round(left_elbow_angle,2)), (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 
   
    #Evaluating the posture for the left hand using a function
    stats, flag_right_left, flag_wrong_left = lateral_posture_left(left_deviation, flag_right_left, flag_wrong_left, stats)

    #Condition to draw target vectors according to the hand motion direction 
    if reps['flag'] == 1:
      p1, p2, q1, q2 = draw_vector_lateral(image, keypoints, reps["flag"], "left")
      value = maprange((0, 110), (0, 255), left_shoulder_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)
    if reps['flag'] == 0:
      p1, p2, q1, q2 = draw_vector_lateral(image, keypoints, reps["flag"], "left")
      value = maprange((110, 0), (0, 255), left_shoulder_angle)
      yellow = 255 - value
      green = 0 + value
      dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
      dotted_line(image, tuple(q1), q2, (0,green,yellow), 3, 10)

    return(image, stats, reps)

def push_ups(image, keypoints, side, reps):
  
    global direction_flag
    global flag_right
    global flag_wrong

    #Right hand angles calculation
    if side.lower() == "right":
      shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_HIP, LEFT_SHOULDER, LEFT_ELBOW)
      elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_WRIST, LEFT_ELBOW, LEFT_SHOULDER)
      hip_angle, x, y, z = keypoint_angle(keypoints, LEFT_SHOULDER, LEFT_HIP, LEFT_KNEE)
    elif side.lower() == "left":
      shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_ELBOW, RIGHT_SHOULDER, RIGHT_HIP)
      elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST)
      hip_angle, x, y, z = keypoint_angle(keypoints, RIGHT_SHOULDER, RIGHT_HIP, RIGHT_KNEE)

    hip_deviation = abs(180 - hip_angle)
    arm_deviation = abs((elbow_angle - (shoulder_angle + 80)))

    #Rep counter
    #reps = curl_reps(shoulder_angle, elbow_angle, reps)

    #Blank white image to display stats
    stats = cv2.imread("white2.jpg") 

    stats = cv2.putText(stats, "Stats", (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    stats = cv2.putText(stats, "Angle at "+ side +" shoulder: "+ str(round(shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, "Angle at "+ side +" elbow: "+ str(round(elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    stats = cv2.putText(stats, "Angle at "+ side +" hip: "+ str(round(hip_angle,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    
    #Evaluating the posture for the right hand using a function
    image, stats, flag_right, flag_wrong = pushups_posture(image, keypoints, side, shoulder_angle, elbow_angle, stats, arm_deviation, hip_deviation)

    #Condition to draw target vectors according to the hand motion direction
    if direction_flag == 1:
        p1, p2 = draw_vector_bicep_curl(image, keypoints, direction_flag, side)
        value = maprange((95, 0), (0, 255), elbow_angle-65)
        yellow = 255 - value
        green = 0 + value
        dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
    elif direction_flag == 0:
        p1, p2 = draw_vector_bicep_curl(image, keypoints, direction_flag, side)
        value = maprange((0, 95), (0, 255), elbow_angle-65)
        yellow = 255 - value
        green = 0 + value
        dotted_line(image, tuple(p1), p2, (0,green,yellow), 3, 10)
    
    return(image, stats, reps)