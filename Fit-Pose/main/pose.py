# External imports
import time
import numpy as np
import cv2
from imutils.video import WebcamVideoStream
import mediapipe as mp

# Local imports
from .data_viz import *
from main.exfunc import bicep_curl, shoulder_press, lateral_raise,push_ups
from main.rep_counter import initialize_reps, update_reps 
from main.basics import *
from . import custom_drawing_utils
from . import custom_pose
from main.basics import initialize_stats, initialize_messages

reps = {}
initialize_reps(reps)
stats_dict = {}
messages = {}

def main_pose(cap, exercise_id, stats_dict, reps, messages, side="right", exit_rep_count=4):

    exercise_id = int(exercise_id)
    if exercise_id == 1:
      exercise_name = "ohp"
    elif exercise_id == 2:
      exercise_name = "bicep_curl"
    elif exercise_id == 3:
      exercise_name = "lateral_raise"
    elif exercise_id == 4:
      exercise_name = "push_ups"
   
    
    initialize_stats(stats_dict)
    initialize_messages(messages)

    mp_drawing = custom_drawing_utils   #Using our own custom version of the drawing functions file
    mp_pose = custom_pose

    with mp_pose.Pose(
        static_image_mode=False,
        upper_body_only=False,
        smooth_landmarks=True,
        min_detection_confidence=0.9,
        min_tracking_confidence=0.9) as pose:
      
      stats = cv2.imread("white2.jpg") 

      while True:
        start = time.time()
        image = cap.read()
        
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        #Creating a list of dictionaries of the keypoints (x,y,z,visibility)
        if results.pose_landmarks:

          keypoints = []
          for data_point in results.pose_landmarks.landmark:
            keypoints.append({
              "X": data_point.x,
              "Y": data_point.y,
              "Z": data_point.z,
              "Visibility": data_point.visibility,
            })

          if exercise_name.lower() == "bicep_curl":
            image, stats_dict, reps, messages = bicep_curl(image, keypoints, side, reps, stats_dict, messages)

          elif exercise_name.lower() == "ohp": 
            image, stats_dict, reps, messages = shoulder_press(image, keypoints, reps, stats_dict, messages)
          
          elif exercise_name.lower() == "lateral_raise":
            image, stats_dict, reps, messages = lateral_raise(image, keypoints, reps, stats_dict, messages)

          elif exercise_name.lower() == "pushups":
            image, stats, stats_dict, reps, messages = push_ups(image, keypoints, side, reps, stats_dict, messages)
          

        else:
          messages[0] = "Stand in view of the camera"
          reps['flag'] = -1
        

        #Conditions to decide on which keypoint connections frozenset to use
        if exercise_name.lower=="full":  
          mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        if exercise_name.lower()=="upper":
          mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
        
        if exercise_name.lower() == "bicep_curl":
            if side.lower() == "right":
              mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.BICEP_CURL_RIGHT)
            elif side.lower() == "left":
              mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.BICEP_CURL_LEFT)

        if exercise_name.lower() == "ohp" or exercise_name.lower() == "lateral_raise":
          mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.OHP)

        if exercise_name.lower() == "squats":
          mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.SQUATS)

        if exercise_name.lower() == "pushups":
          mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.PUSHUPS)
        
        end = time.time()
        fps = round((1/(end-start)),2)
          
        return image, stats_dict, reps, messages
