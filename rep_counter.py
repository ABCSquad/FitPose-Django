# Imports
import time

# Initializing variables related to reps in a dict
def initialize_reps(reps):
    reps['count'] = 0
    reps['flag'] = -1
    reps['time'] = {}
    reps['correct_form'] = {}
    reps['wrong_form'] = {}

# For counting no. of frames in correct or wrong form for each rep
def checkForm(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 0

# Counting reps for ohp
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps):

    if right_deviation < 15 and left_deviation < 15:

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
        checkForm(reps['correct_form'], reps['count'])

        if elbow_angle > 160 and reps['flag'] == 0:
            reps['flag'] = 1
            reps['count'] += 1
            reps['time'][reps['count']] = time.time()

        elif elbow_angle < 65 and (reps['flag'] == 1 or reps['flag'] == -1):
            reps['flag'] = 0

    else:
        checkForm(reps['wrong_form'], reps['count'])
            
    return reps
