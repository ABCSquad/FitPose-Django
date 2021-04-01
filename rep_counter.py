# Basic imports
import cv2
from imutils.video import WebcamVideoStream
import numpy as np

# Importing mediapipe
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


# Setting initial reps and flag to 0
reps = 0
flag = 0


# Counting reps for ohp using angles
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps, rep_flag):

    if right_deviation < 10 and left_deviation < 10:
        if right_shoulder_angle < 90 and left_shoulder_angle < 90 and rep_flag == 0:
            rep_flag = 1
        elif right_shoulder_angle > 170 and left_shoulder_angle > 170 and rep_flag == 1:
            rep_flag = 0
            reps += 1

    return reps, rep_flag


# Counting reps for bicep curls using angles
def curl_reps(shoulder_angle, elbow_angle, reps, rep_flag):

    if shoulder_angle<13 or shoulder_angle>355 and rep_flag == 0:
        if elbow_angle > 160:
            rep_flag = 1
        elif elbow_angle < 65 and rep_flag == 1:
            rep_flag = 0
            reps += 1

    return reps, rep_flag


# Loading knn classifier model
def load_model(model_path):
    import pickle
    model = pickle.load(open(model_path, 'rb'))
    return model

model_path = './models/knn_ohp'
model = load_model(model_path)


# For reshaping pose_landmarks before passing though knn model
def reshape_landmarks(pose_landmarks):
    assert len(pose_landmarks.landmark) == 25, 'Unexpected number of predicted pose landmarks: {}'.format(len(pose_landmarks.landmark))
    pose_landmarks = [[lmk.x, lmk.y] for lmk in pose_landmarks.landmark]
    pose_landmarks = np.reshape(np.around(pose_landmarks[11:17], 5).flatten().astype(np.float64).tolist(), (1, -1))
    return pose_landmarks


# For counting reps using knn
def count_reps(model, pose_landmarks, reps, flag):

    probability = model.predict_proba(pose_landmarks)
    # print(probability)

    if probability[0][0] == 1 and flag == 0:
        flag = 1

    elif probability[0][1] == 1 and flag == 1:
        reps += 1
        flag = 0

    return reps, flag


# For webcam input:
def webcam_input(reps, flag):
    cap = WebcamVideoStream(src=1).start()
    with mp_pose.Pose(

        upper_body_only = True,
        static_image_mode=False,
        smooth_landmarks=True,
        min_detection_confidence=0.9,
        min_tracking_confidence=0.9) as pose:
      
        while True:

            image = cap.read()
          
            # Flip the image horizontally for a later selfie-view display, and convert the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # Display reps at down left corner
            cv2.putText(image, f'Reps: {reps}', (10, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

            # To improve performance, optionally mark the image as not writeable to pass by reference.
            image.flags.writeable = False
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.UPPER_BODY_POSE_CONNECTIONS)
            
            # Passing key points through model
            pose_landmarks = results.pose_landmarks
            if pose_landmarks is not None:
                pose_landmarks = reshape_landmarks(pose_landmarks)
                reps, flag = count_reps(model, pose_landmarks, reps, flag)

            cv2.imshow('FitPose', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break


# Running main
if __name__ == '__main__':
    webcam_input(reps, flag)
