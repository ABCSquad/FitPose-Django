# Basic imports
import cv2
import time
from imutils.video import WebcamVideoStream
import numpy as np
import pickle

# Importing mediapipe
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Loading knn classifier model
model_path = './dataset_out/ohp/knn_ohp'
model = pickle.load(open(model_path, 'rb'))

# Setting initial reps to 0
reps = 0
flag = 0

# For webcam input:
cap = WebcamVideoStream(src=0).start()
with mp_pose.Pose(

    upper_body_only = True,
    static_image_mode=False,
    smooth_landmarks=True,
    min_detection_confidence=0.9,
    min_tracking_confidence=0.9) as pose:
  
    while True:

        # start = time.time()
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
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
        cv2.imshow('FitPose', image)
        
        # Passing key points through model
        pose_landmarks = results.pose_landmarks
        if pose_landmarks is not None:
            assert len(pose_landmarks.landmark) == 25, 'Unexpected number of predicted pose landmarks: {}'.format(len(pose_landmarks.landmark))
            pose_landmarks = [[lmk.x, lmk.y] for lmk in pose_landmarks.landmark]
            pose_landmarks = np.reshape(np.around(pose_landmarks[11:17], 5).flatten().astype(np.float64).tolist(), (1, -1))

            prediction = model.predict(pose_landmarks)
            probability = model.predict_proba(pose_landmarks)

            # Counting reps
            if probability[0][0] == 1 and flag == 0:
                flag = 1

            elif probability[0][1] == 1 and flag == 1:
                reps += 1
                flag = 0
                print(reps)

        # end = time.time()
        # print(1/(end-start))

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
