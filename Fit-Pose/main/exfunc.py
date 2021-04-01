import numpy as np
import math
import cv2


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

flag_wrong = 0
flag_right = 0
flag_right_left = 0
flag_wrong_left = 0


#Angle using dot product
# def angle(a,b,c): 
#     ba = a - b
#     bc = c - b

#     cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
#     angle = np.arccos(cosine_angle)

#     return(np.degrees(angle))

#Angle using arctan2
def angle(a,b,c):
    ba = a - b
    bc = c - b
    angle = math.atan2(bc[1], bc[0]) - math.atan2(ba[1], ba[0])
    if (angle < 0):
        angle += 2 * math.pi
    angle_in_deg = (angle*180)/math.pi
    return angle_in_deg
      
#Used for calculating angle between 3 specified keypoints 
def keypoint_angle(keypoints,a,b,c):
    a1 = keypoints[a]['X']*100,keypoints[a]['Y']*100
    b1 = keypoints[b]['X']*100,keypoints[b]['Y']*100
    c1 = keypoints[c]['X']*100,keypoints[c]['Y']*100
    a2,b2,c2 = np.array(list(a1)), np.array(list(b1)), np.array(list(c1))
    angle1 = angle(a2,b2,c2)
    return(angle1,a2,b2,c2)

def shoulder_press(keypoints):

    #Declaration of global flags
    global flag_wrong
    global flag_right
    global flag_right_left 
    global flag_wrong_left

    #Right hand 
    right_shoulder_angle, x, y, z = keypoint_angle(keypoints, LEFT_ELBOW, LEFT_SHOULDER, LEFT_HIP)
    right_elbow_angle, x, y, z = keypoint_angle(keypoints, LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST)
    right_deviation = abs(right_shoulder_angle - right_elbow_angle)

    #Left hand
    left_shoulder_angle, x, y, z = keypoint_angle(keypoints, RIGHT_HIP, RIGHT_SHOULDER, RIGHT_ELBOW)
    left_elbow_angle, x, y, z = keypoint_angle(keypoints, RIGHT_WRIST, RIGHT_ELBOW, RIGHT_SHOULDER)
    left_deviation = abs(left_shoulder_angle - left_elbow_angle)

    #Image Processing
    stats = cv2.imread('white2.jpg') 
    stats = cv2.putText(stats, 'Stats', (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)

    #Angles of right hand
    stats = cv2.putText(stats, 'Angle at right shoulder : '+ str(round(right_shoulder_angle,2)), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, 'Angle at right elbow : '+ str(round(right_elbow_angle,2)), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 

    #Deviation conditions
    if right_deviation<10:
      stats = cv2.putText(stats, 'Right deviation: '+ str(round(right_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA)
      flag_right += 1
      if flag_right>0 and flag_right<=20:
        stats = cv2.putText(stats, 'Fix your right hand form!', (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
      elif flag_right>20:
        flag_wrong = 0
        stats = cv2.putText(stats, 'Your right hand form is perfect', (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
    else:
      stats = cv2.putText(stats, 'Right deviation: '+ str(round(right_deviation,2)), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)
      flag_wrong+=1
      if flag_wrong>0 and flag_wrong<=15:
        stats = cv2.putText(stats, 'Your right hand form is perfect', (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
      elif flag_wrong>15:
        flag_right = 0
        stats = cv2.putText(stats, 'Fix your right hand form!', (5,185), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)

    #Angles of left hand
    stats = cv2.putText(stats, 'Angle at left shoulder : '+ str(round(left_shoulder_angle,2)), (5,115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
    stats = cv2.putText(stats, 'Angle at left elbow : '+ str(round(left_elbow_angle,2)), (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 

    #Deviation conditions
    if left_deviation<10:
      stats = cv2.putText(stats, 'Left deviation: '+ str(round(left_deviation,2)), (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA) 
      flag_right_left += 1
      if flag_right_left>0 and flag_right_left<=20:
        stats = cv2.putText(stats, 'Fix your left hand form!', (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)
      elif flag_right_left>20:
        flag_wrong_left = 0
        stats = cv2.putText(stats, 'Your left hand form is perfect', (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
    else:
      stats = cv2.putText(stats, 'Left deviation: '+ str(round(left_deviation,2)), (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA) 
      flag_wrong_left+=1
      if flag_wrong_left>0 and flag_wrong_left<=15:
        stats = cv2.putText(stats, 'Your left hand form is perfect', (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2, cv2.LINE_AA)
      elif flag_wrong_left>15:
        flag_right_left  = 0
        stats = cv2.putText(stats, 'Fix your left hand form!', (5,205), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2, cv2.LINE_AA)

    return(right_shoulder_angle, right_elbow_angle, right_deviation, left_shoulder_angle, left_elbow_angle, left_deviation, stats)
    