import cv2
import mediapipe as mp
import time
from imutils.video import WebcamVideoStream
import numpy as np
from exfunc import *
import cv2
from rep_counter import *

# Loading knn model
model_path = "./models/knn_ohp"
model = load_model(model_path)

# Setting initial reps and flag to 0
reps = 0
rep_flag = 0

#time.sleep(5)
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# For webcam input:
cap = WebcamVideoStream(src=1).start()

upper = True
with mp_pose.Pose(
    static_image_mode=False,
    upper_body_only=upper,
    smooth_landmarks=True,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as pose:
  
  stats = cv2.imread("white2.jpg") 

  while True:
    start = time.time()
    image = cap.read()
    # stats = cv2.imread("white2.jpg") 
    
    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    # Display reps at down left corner
    cv2.putText(image, f"Reps: {reps}", (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

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
          "X": data_point.x,
          "Y": data_point.y,
          "Z": data_point.z,
          "Visibility": data_point.visibility,
        })
      stats, reps, rep_flag = bicep_curl(keypoints, "right", reps, rep_flag)

    else:
      image = cv2.putText(image, "Upper body not visible", (5,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255), 2, cv2.LINE_AA)
    if upper==False:  
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    elif upper==True:
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
    
    # print(flag_wrong,"", flag_right)

    # Passing key points through model
    # pose_landmarks = results.pose_landmarks
    # if pose_landmarks is not None:
      # pose_landmarks = reshape_landmarks(pose_landmarks)
      # reps, flag = count_reps(model, pose_landmarks, reps, flag)
    
    end = time.time()
    #print(1/(end-start))
    if stats is not None:
      cv2.imshow("Stats", stats)
    image = cv2.putText(image, str(round((1/(end-start)),2)), (565,25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2, cv2.LINE_AA)
    cv2.imshow("MediaPipe Pose", image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
    

cap.stop()
