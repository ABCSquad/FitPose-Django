import time

# Counting reps for ohp
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, rep):

    if right_deviation < 10 and left_deviation < 10:
        if right_shoulder_angle < 90 and left_shoulder_angle < 90 and rep['flag'] == 0:
            rep['flag'] = 1
            rep['no'] += 1
        elif right_shoulder_angle > 170 and left_shoulder_angle > 170 and (rep['flag'] == 1 or rep['flag'] == -1):
            rep['flag'] = 0

    return rep


# Counting reps for bicep curls
def curl_reps(shoulder_angle, elbow_angle, rep):

    if shoulder_angle<13 or shoulder_angle>355: 
        if elbow_angle > 160 and rep['flag'] == 0:
            rep['flag'] = 1
            rep['no'] += 1
            rep['time']['no'] = time.time()
        elif elbow_angle < 65 and (rep['flag'] == 1 or rep['flag'] == -1):
            rep['flag'] = 0
            
    return rep
