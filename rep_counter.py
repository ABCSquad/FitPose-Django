# Imports
import time


'''
HELPER FUNCITONS -
These functions are called and used within or surrounding the exercise specific functions to aid them in carrying out their different operations.
'''


# Initializing variables related to reps in a dict
def initialize_reps(reps):
    reps['count'] = -1
    reps['flag'] = -1
    reps['timestamp'] = {}
    reps['time'] = {}
    reps['correct_form'] = {}
    reps['wrong_form'] = {}


# For initializing correct_form and wrong_form dicts for each succesful rep 
def check_key(dict1, dict2, key):
    if key not in dict1:
        dict1[key] = 0
    if key not in dict2:
        dict2[key] = 0


# For converting starting timestamps of reps to time taken for each rep
def get_rep_time(reps):
    for i in range(reps['count']):
        if reps['count'] >= 0:
            reps['time'][i+1] = reps['timestamp'][i+1] - reps['timestamp'][i]


# For converting dict values from no. of frames to time in seconds
def frames_to_time(reps):
    for i in range(reps['count']):
        if reps['count'] >= 0:
            reps['correct_form'][i] = reps['time'][i+1] * reps['correct_form'][i] / (reps['correct_form'][i] + reps['wrong_form'][i])
            reps['wrong_form'][i] = reps['time'][i+1] - reps['correct_form'][i]


# For incrementing value of correct form or wrong form after the user has assumed initial stance and the exercise has commenced
def form_increment(reps, form):
        if reps['count'] >= 0:
            reps[form][reps['count']] += 1


# For incrementng rep count and changing related variables once a succesful rep has been executed
def rep_increment(reps):
    reps['flag'] = 1
    reps['count'] += 1
    reps['timestamp'][reps['count']] = time.time()


# To call required functions to perform calculations after exercise loop is over in main function
def update_reps(reps):
    get_rep_time(reps)
    frames_to_time(reps)


'''
EXERCISE SPECIFIC FUNCITONS - 
These functions are directly called by the main program depending on the exercise that the user selects and wishes to perform.
'''


# Counting reps for ohp
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps):

    check_key(reps['correct_form'],reps['wrong_form'],reps['count'])

    if right_deviation < 15 and left_deviation < 15:
        form_increment(reps,'correct_form')

        if right_shoulder_angle < 90 and left_shoulder_angle < 90 and reps['flag'] == 0:
            rep_increment(reps)

        elif right_shoulder_angle > 170 and left_shoulder_angle > 170 and (reps['flag'] == 1 or reps['flag'] == -1):
            reps['flag'] = 0

    else:
        form_increment(reps,'wrong_form')

    return reps


# Counting reps for bicep curls
def curl_reps(shoulder_angle, elbow_angle, reps):

    check_key(reps['correct_form'],reps['wrong_form'],reps['count'])

    if shoulder_angle < 13 or shoulder_angle > 355 : 
        form_increment(reps,'correct_form')

        if elbow_angle > 160 and (reps['flag'] == 0 or reps['flag'] == -1):
            rep_increment(reps)

        elif elbow_angle < 65 and reps['flag'] == 1:
            reps['flag'] = 0

    else:
        form_increment(reps,'wrong_form')
            
    return reps
