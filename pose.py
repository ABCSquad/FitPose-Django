import cv2
import mediapipe as mp
import time
from imutils.video import WebcamVideoStream
import numpy as np
from exfunc import *
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# For webcam input:
cap = WebcamVideoStream(src=0).start()

upper = True
with mp_pose.Pose(
    static_image_mode=False,
    upper_body_only=upper,
    smooth_landmarks=True,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as pose:
  
  
  while True:
    start = time.time()
    image = cap.read()
    stats = cv2.imread('white2.jpg') 
  

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #Creating a uper_body_only yes/no state

    #Creating a list of dictionaries of the keypoints (x,y,z,visibility)
    if results.pose_landmarks:
      keypoints = []
      for data_point in results.pose_landmarks.landmark:
        keypoints.append({
          'X': data_point.x,
          'Y': data_point.y,
          'Z': data_point.z,
          'Visibility': data_point.visibility,
        })
      right_shoulder_angle, right_elbow_angle, right_deviation, left_shoulder_angle, left_elbow_angle, left_deviation = shoulder_press(keypoints)
      stats = cv2.putText(stats, 'Angle at right shoulder : '+ str(right_shoulder_angle), (5,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
      stats = cv2.putText(stats, 'Angle at right elbow : '+ str(right_elbow_angle), (5,55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 
      if right_deviation<10:
        stats = cv2.putText(stats, 'Right deviation: '+ str(right_deviation), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA)
      else:
        stats = cv2.putText(stats, 'Right deviation: '+ str(right_deviation), (5,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)

      stats = cv2.putText(stats, 'Angle at left shoulder : '+ str(left_shoulder_angle), (5,115), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)    
      stats = cv2.putText(stats, 'Angle at left elbow : '+ str(left_elbow_angle), (5,135), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA) 
      if left_deviation<10:
        stats = cv2.putText(stats, 'Left deviation: '+ str(left_deviation), (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2, cv2.LINE_AA) 
      else:
        stats = cv2.putText(stats, 'Left deviation: '+ str(left_deviation), (5,155), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA) 
    else:
      image = cv2.putText(image, 'Upper body not visible', (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2, cv2.LINE_AA)
    if upper==False:  
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    elif upper==True:
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)
    
    end = time.time()
    #print(1/(end-start))
    stats = cv2.putText(stats, 'FPS : '+ str(1/(end-start)), (5,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    cv2.imshow('Stats', stats)
    if cv2.waitKey(5) & 0xFF == 27:
      break
    

cap.stop()
