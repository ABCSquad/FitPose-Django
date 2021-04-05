import time

# Counting reps for ohp
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps):

    if right_deviation < 10 and left_deviation < 10:

        if right_shoulder_angle < 90 and left_shoulder_angle < 90 and reps['flag'] == 0:
            reps['flag'] = 1
            reps['count'] += 1
            reps['time'][reps['count']] = time.time()

        elif right_shoulder_angle > 170 and left_shoulder_angle > 170 and (reps['flag'] == 1 or reps['flag'] == -1):
            reps['flag'] = 0

    return reps


# Counting reps for bicep curls
def curl_reps(shoulder_angle, elbow_angle, reps):

    if shoulder_angle<13 or shoulder_angle>355: 

        if elbow_angle > 160 and reps['flag'] == 0:
            reps['flag'] = 1
            reps['count'] += 1
            reps['time'][reps['count']] = time.time()

        elif elbow_angle < 65 and (reps['flag'] == 1 or reps['flag'] == -1):
            reps['flag'] = 0
            
    return reps
