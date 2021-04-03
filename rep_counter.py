# Counting reps for ohp
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps, rep_flag):

    if right_deviation < 10 and left_deviation < 10:
        if right_shoulder_angle < 90 and left_shoulder_angle < 90 and rep_flag == 0:
            rep_flag = 1
        elif right_shoulder_angle > 170 and left_shoulder_angle > 170 and rep_flag == 1:
            rep_flag = 0
            reps += 1

    return reps, rep_flag


# Counting reps for bicep curls
def curl_reps(shoulder_angle, elbow_angle, reps, rep_flag):

    if shoulder_angle<13 or shoulder_angle>355 and rep_flag == 0:
        if elbow_angle > 160:
            rep_flag = 1
        elif elbow_angle < 65 and rep_flag == 1:
            rep_flag = 0
            reps += 1
            
    return reps, rep_flag
