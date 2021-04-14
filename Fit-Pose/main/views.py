from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import StreamingHttpResponse
from main.camera import VideoCamera, gen
from .models import  Detail, Video
import json 
from random import randint 
from time import sleep
from django.core.serializers.json import  DjangoJSONEncoder
import time
from django.views import View

# Create your views here.
detailid = 0

def app(request, detail_id):
	global detailid
	detailid = detail_id
	video = get_object_or_404(Video, pk=detail_id)
	return render(request, 'main/app.html',{'id':detail_id,'videos':video})




def webcam_feed(request):
	global detailid
	return StreamingHttpResponse(gen(VideoCamera(),detailid),
					content_type='multipart/x-mixed-replace; boundary=frame')


class realtime:

	def rl(self):
		for i in range(1000):
			message = {'message': randint(1, 100)}
			return message
			

def gene(real):

	initial_data = ""
	while True:
		data = json.dumps(dict((real.rl())),cls=DjangoJSONEncoder)
		if not initial_data == data:
			yield "\ndata: {}\n\n".format(data) 
			initial_data = data
		time.sleep(1)




class realtime_feed(View):

	def get(self, request):
		response = StreamingHttpResponse(gene(realtime()))
		response['Content-Type'] = 'text/event-stream'
		return response
