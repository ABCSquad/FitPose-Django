#THIS WILL INCLLUDE PLAYLIST


from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.playlist, name="playlist"),
]

