from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import StreamingHttpResponse
from main.camera import *
from .models import  Detail, Video
import time
from django.views import View
from .models import Session, Stats
from exercises.models import Detail
from django.views.generic import TemplateView

# Create your views here.
detailid = 0
try:
    print(reps_global['count'])
except:
    pass

def start_session(request, detail_id):
    user_id = request.user
    ex_id = Detail.objects.get(id=detail_id)
    session = Session(user=user_id, exercise=ex_id)
    session.save()


def app(request, detail_id):

    if request.method == 'POST':
        repAbort = request.POST['repAbort']
        abortFlagSwitch()
        time.sleep(0.5)
        if int(repAbort)==0:
            return redirect('exercises')
        return redirect('main:result')
    else:
        start_session(request, detail_id)
        global detailid
        detailid = detail_id
        video = get_object_or_404(Video, detail_id=detail_id)
        return render(request, 'main/app.html',{'id':detail_id,'videos':video})

# def result(request):
# 	return render(request, 'main/result.html')


def webcam_feed(request):
    global detailid
    return StreamingHttpResponse(gen(VideoCamera(),detailid),
                    content_type='multipart/x-mixed-replace; boundary=frame')


class realtime_feed(View):

    def get(self, request):
        temp = gene(realtime())
        response = StreamingHttpResponse(temp)

        response['Content-Type'] = 'text/event-stream'
        return response

class ResultChartView(TemplateView):
    template_name="main/result.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ses_id = Stats.objects.latest('id').session_id
        context["qs"] = Stats.objects.filter(session_id=ses_id)

        return context
