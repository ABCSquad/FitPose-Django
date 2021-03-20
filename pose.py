import cv2
import mediapipe as mp
import time
from imutils.video import WebcamVideoStream

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# For webcam input:
cap = WebcamVideoStream(src=0).start()
upper = False
with mp_pose.Pose(
    static_image_mode=False,
    upper_body_only=upper,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  
  
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

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    #Creating a uper_body_only yes/no state
    if upper==False:
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
    elif upper==True:
      mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
    cv2.imshow('MediaPipe Pose', image)
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
          #print(keypoints[-1]['X'])
          print(keypoints[-1]['X'], " ", keypoints[-1]['Y'])
    end = time.time()
    print(1/(end-start))
    if cv2.waitKey(5) & 0xFF == 27:
      break
    

cap.stop()
