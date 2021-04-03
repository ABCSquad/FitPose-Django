import cv2
from body_parts import *
import numpy as np

#Function maps a range a to b and returns the output for a value 's' from range a
def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

#Function for ball tracking for bicep curls
def curl_ball(keypoints, image, angle, movement, side):

    #Condition that changes the colour and thickness according to the motion of the hand
    if movement.lower() == "up":
        value = maprange((160, 65), (0, 255), angle)
        thickness = maprange((160, 65), (20, 60), angle)
    elif movement.lower() == "down":
        value = maprange((65, 160), (0, 255), angle)
        thickness = maprange((65, 160), (20, 60), angle)

    #Changing the elbow according the which hand is being used
    if side.lower() == "left":
        position = [keypoints[RIGHT_ELBOW]['X'], keypoints[RIGHT_ELBOW]['Y']]
    elif side.lower() == "right":
        position = [keypoints[LEFT_ELBOW]['X'], keypoints[LEFT_ELBOW]['Y']]

    #Scaling the model output values to the frame's height and width 
    frame_height, frame_width = image.shape[:2]
    position *= np.array([frame_width, frame_height])
    position = np.around(position, 5).flatten().astype(np.int).tolist()    

    #Varying the shade of red and green   
    green = 0 + int(value)
    red = 255 - int(value)
    color = (0, green, red)

    #Drawing the circle according to the dynamic data
    cv2.circle(image, tuple(position), 1, color, int(thickness))

    return image








