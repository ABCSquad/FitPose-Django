import cv2
from imutils.video import WebcamVideoStream
from main.pose import main_pose
import json 
from random import randint 
import time
from django.core.serializers.json import  DjangoJSONEncoder

stats_dict_global = {}
reps_global = {}
messages_global = {}

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

    while True:
        stats_dict = {}
        reps = {}
        messages = {}
        frame = camera.get_frame(detail_id, stats_dict, reps, messages)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def gene(real):

    initial_data = ""
    while True:
        data = json.dumps(list((real.rl()).values()),cls=DjangoJSONEncoder)
        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data) 
            initial_data = data
        time.sleep(0.001)

class realtime:
    def rl(self):
        global stats_dict_global
        global reps_global
        global messages_global

        for i in range(1000):
            # print(messages_global)
            # print(reps_global)
            message = messages_global
            return message