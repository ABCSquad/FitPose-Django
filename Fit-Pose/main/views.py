from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from main.camera import VideoCamera, gen

# Create your views here.


def app(request):
    return render(request, 'main/app.html')

def webcam_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()),
					content_type='multipart/x-mixed-replace; boundary=frame')
