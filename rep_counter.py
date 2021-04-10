# Imports
import time


'''
HELPER FUNCITONS -
These functions are called and used within or surrounding the exercise specific functions to aid them in carrying out their different operations.
'''


# Initializing variables related to reps in a dict
def initialize_reps(reps):
    reps['count'] = -1         # No. of reps
    reps['flag'] = -1          # Flag that changes every time an exercise reaches its terminal state
    reps['timestamp'] = {}     # time.time() saved at the beginning of every rep
    reps['time'] = {}          # Time taken for each rep
    reps['frame'] = 0          # No. of frames
    reps['correct_form'] = {}  # No. of frames in correct form for each rep
    reps['wrong_form'] = {}    # No. of frames in wrong form for each rep
    reps['frame_form'] = {}    # Form in each frame


# For checking if key exists in dict
def check_key(dict, key, value):
    if key not in dict:
        dict[key] = value


# To initialize dicts values for correct_form, wrong_form and frame_form
def initialize_dicts(reps):
    if reps['count'] >= 0:
        check_key(reps['correct_form'],reps['count'],0)
        check_key(reps['wrong_form'],reps['count'],0)
        check_key(reps['frame_form'],reps['count'],{})


# For incrementing value (which is the no. of frames) of correct form or wrong form after the user has assumed initial stance and the exercise has commenced
# Also for checking form in each frame for each rep
def form_increment(reps, form):
    if reps['count'] >= 0:
        reps[form][reps['count']] += 1
        reps['frame_form'][reps['count']][reps['frame']] = form
        reps['frame'] += 1
            

# For incrementng rep count and changing related variables once a succesful rep has been executed
def rep_increment(reps):
    reps['flag'] = 1
    reps['count'] += 1
    reps['timestamp'][reps['count']] = time.time()


# For converting correct_form and wrong_form values from no. of frames to time in seconds
def frames_to_time(reps):
    if reps['count'] >= 0:
        for i in range(reps['count']):
            reps['time'][i+1] = reps['timestamp'][i+1] - reps['timestamp'][i] # For converting starting timestamps of reps to time taken for each rep
            reps['correct_form'][i] = reps['time'][i+1] * reps['correct_form'][i] / (reps['correct_form'][i] + reps['wrong_form'][i])
            reps['wrong_form'][i] = reps['time'][i+1] - reps['correct_form'][i]


# To call required functions to perform calculations after exercise loop is over in main function
def update_reps(reps):
    frames_to_time(reps)


'''
EXERCISE SPECIFIC FUNCITONS - 
These functions are directly called by the main program depending on the exercise that the user selects and wishes to perform.
'''


# Counting reps for over head press
def ohp_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps):

    initialize_dicts(reps)

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

    initialize_dicts(reps)

    if shoulder_angle < 13 or shoulder_angle > 355 : 
        form_increment(reps,'correct_form')

        if elbow_angle > 160 and (reps['flag'] == 0 or reps['flag'] == -1):
            rep_increment(reps)

        elif elbow_angle < 65 and reps['flag'] == 1:
            reps['flag'] = 0

    else:
        form_increment(reps,'wrong_form')
            
    return reps


# Counting reps for lateral raises
def lateral_reps(right_deviation, left_deviation, right_shoulder_angle, left_shoulder_angle, reps):

    initialize_dicts(reps)

    if right_deviation < 15 and left_deviation < 15:
        form_increment(reps,'correct_form')

        if right_shoulder_angle < 20 and left_shoulder_angle < 20 and (reps['flag'] == 0 or reps['flag'] == -1):
            rep_increment(reps)

        elif right_shoulder_angle > 90 and left_shoulder_angle > 90 and reps['flag'] == 1:
            reps['flag'] = 0

    else:
        form_increment(reps,'wrong_form')

    return reps
