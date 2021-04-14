import cv2
from imutils.video import WebcamVideoStream
from main.pose import main_pose

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
    
    def get_frame(self, detail_id, stats_dict, reps):
        image, stats_dict = main_pose(self.cap, detail_id, stats_dict, reps)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


def gen(camera, detail_id):

    while True:
        stats_dict = {}
        reps = {}
        frame = camera.get_frame(detail_id, stats_dict, reps)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')