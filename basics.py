import numpy as np
import math
import cv2

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

def ohp_posture_right(right_deviation, flag_right, flag_wrong, stats):
    if right_deviation<10:
      stats = cv2.putText(stats, "Right deviation: "+ str(round(right_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA)
      flag_right += 1
      if flag_right>0 and flag_right<=20:
        stats = cv2.putText(stats, "Fix your right hand form!", (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
      elif flag_right>20:
        flag_wrong = 0
        stats = cv2.putText(stats, "Your right hand form is perfect", (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
    else:
      stats = cv2.putText(stats, "Right deviation: "+ str(round(right_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)
      flag_wrong+=1
      if flag_wrong>0 and flag_wrong<=15:
        stats = cv2.putText(stats, "Your right hand form is perfect", (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
      elif flag_wrong>15:
        flag_right = 0
        stats = cv2.putText(stats, "Fix your right hand form!", (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    return(stats, flag_right, flag_wrong)

def ohp_posture_left(left_deviation, flag_right_left, flag_wrong_left, stats):
    if left_deviation<10:
      stats = cv2.putText(stats, "Left deviation: "+ str(round(left_deviation,2)), (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA) 
      flag_right_left += 1
      if flag_right_left>0 and flag_right_left<=20:
        stats = cv2.putText(stats, "Fix your left hand form!", (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
      elif flag_right_left>20:
        flag_wrong_left = 0
        stats = cv2.putText(stats, "Your left hand form is perfect", (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
    else:
      stats = cv2.putText(stats, "Left deviation: "+ str(round(left_deviation,2)), (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA) 
      flag_wrong_left+=1
      if flag_wrong_left>0 and flag_wrong_left<=15:
        stats = cv2.putText(stats, "Your left hand form is perfect", (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
      elif flag_wrong_left>15:
        flag_right_left  = 0
        stats = cv2.putText(stats, "Fix your left hand form!", (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    return(stats, flag_right_left, flag_wrong_left)

def curl_posture(shoulder_angle, elbow_angle, stats, direction_flag):
    if shoulder_angle>180:
        upper_arm_deviation = abs(shoulder_angle - 360)
    else:
        upper_arm_deviation = shoulder_angle

    if shoulder_angle<13 or shoulder_angle>355:
        stats = cv2.putText(stats, "Upper arm deviation: "+ str(round(upper_arm_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA)
        stats = cv2.putText(stats, "Your upper arm position is perfect", (5,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
        if elbow_angle > 160:
            stats = cv2.putText(stats, "Lift your forearm", (5,125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
            direction_flag = 1
        elif elbow_angle < 160 and elbow_angle > 65:
            stats = cv2.putText(stats, "Your forearm posture is perfect", (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
            stats = cv2.putText(stats, "Complete the rep!", (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
        else:
            stats = cv2.putText(stats, "Lower your forearm", (5,125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
            direction_flag = 0
    else:
        stats = cv2.putText(stats, "Upper arm deviation: "+ str(round(upper_arm_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)
        stats = cv2.putText(stats, "Your upper arm is not parallel to your torso", (5,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    
    return(stats, direction_flag)

def tricep_extension_posture(shoulder_angle, elbow_angle, stats):
    upper_arm_deviation = abs(shoulder_angle - 180)
    
    if shoulder_angle>160 and shoulder_angle<180:
        stats = cv2.putText(stats, "Upper arm deviation: "+ str(round(upper_arm_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA)
        stats = cv2.putText(stats, "Your upper arm position is perfect", (5,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
        if elbow_angle < 70:
            stats = cv2.putText(stats, "Lift your forearm", (5,125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
        elif elbow_angle < 160 and elbow_angle >= 70:
            stats = cv2.putText(stats, "Your forearm posture is perfect", (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
            stats = cv2.putText(stats, "Complete the rep!", (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2, cv2.LINE_AA)
        else:
            stats = cv2.putText(stats, "Lower your forearm", (5,125), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    else:
        stats = cv2.putText(stats, "Upper arm deviation: "+ str(round(upper_arm_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)
        stats = cv2.putText(stats, "Your upper arm is not parallel to your torso", (5,105), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
    
    return(stats)
