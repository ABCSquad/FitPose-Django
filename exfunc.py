import numpy as np

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

count = 0
flag = -1

def angle(a,b,c): 
    ba = a - b
    bc = c - b

    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)

    return(np.degrees(angle))
      
#Used for calculating angle between 3 specified keypoints 
def keypoint_angle(keypoints,a,b,c):
    a1 = keypoints[a]['X']*100,keypoints[a]['Y']*100
    b1 = keypoints[b]['X']*100,keypoints[b]['Y']*100
    c1 = keypoints[c]['X']*100,keypoints[c]['Y']*100
    print(a1,"",b1,"",c1)
    a2,b2,c2 = np.array(list(a1)), np.array(list(b1)), np.array(list(c1))
    angle1 = angle(a2,b2,c2)
    return(angle1,a2,b2,c2)

def shoulder_press(keypoints):
    key_angle, x, y, z = keypoint_angle(keypoints, RIGHT_SHOULDER, LEFT_SHOULDER, LEFT_ELBOW)
    global count,flag
    if key_angle<100:
        if flag==1:
            flag=0
            count += 1
        flag=0
    elif key_angle>165 and z[0]-y[0]>10:
        flag=1
    if count>0:
        return(key_angle,count)
    else:
        return(key_angle, 0)
    