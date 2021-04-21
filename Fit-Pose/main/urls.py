#THIS WILL BE THE MAIN APP
from django.urls import path, include
from . import views
from .views import realtime_feed
from main.views import ResultChartView
<<<<<<< HEAD
=======

>>>>>>> akash

app_name = 'main'

urlpatterns = [
    path('<detail_id>/', views.app, name="app"),  
    path('webcam_feed', views.webcam_feed, name='webcam_feed'),
    path('realtime_feed', realtime_feed.as_view(), name='realtime_feed'),
    path('result', ResultChartView.as_view(), name="result"),
]


