import cv2
from imutils.video import WebcamVideoStream
from main.pose import main_pose
import json 
from random import randint 
import time
from .rep_counter import *
from .data_viz import *
from django.core.serializers.json import  DjangoJSONEncoder
from django.shortcuts import redirect
from exercises.views import print_reps

stats_dict_global = {}
reps_global = {}
messages_global = {}
abortFlagGlobal = False

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.cap = WebcamVideoStream(src=0).start()
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.cap.stop()
    
    def get_frame(self, detail_id, stats_dict, reps, messages):
        global stats_dict_global
        global reps_global
        global messages_global

        image, stats_dict, reps, messages = main_pose(self.cap, detail_id, stats_dict, reps, messages)
        stats_dict_global = stats_dict
        reps_global = reps
        messages_global = messages
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera, detail_id):
    global abortFlagGlobal
    abortFlagGlobal = False
    reps = {}
    initialize_reps(reps)
    max_reps = print_reps()

    while reps['count']<int(max_reps) and abortFlagGlobal is False:
        stats_dict = {}
        messages = {}
        frame = camera.get_frame(detail_id, stats_dict, reps, messages)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    update_reps(reps)
    initialize_viz(reps)

def gene(real):

    initial_data = ""
    while True:
        data = json.dumps((real.rl()),cls=DjangoJSONEncoder)
        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data) 
            initial_data = data
        time.sleep(0.1)

class realtime:
    def rl(self):
        global stats_dict_global
        global reps_global
        global messages_global
        max_reps = print_reps()

        reps = reps_global
        message = messages_global
        message = list(message.values())
        
        
        try:
            if reps['count'] != -1:
                message.append(reps['count'])
                if reps ['count'] == max_reps: reps_global['count'] = -1 # To prevent reps_global['count'] from retaining its value and directly going to the results page
            else:
                message.append(int(0))
        except:
            pass

        message.append(max_reps)

        return message

def abortFlagSwitch():
    global abortFlagGlobal
    abortFlagGlobal = not abortFlagGlobal