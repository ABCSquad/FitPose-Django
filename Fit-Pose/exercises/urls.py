#THIS WILL INCLLUDE EXERCISE LIST ALSO REDIRECT TO PLAYLIST


from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.exercises, name="exercises"),
    path('playlist', include('playlist.urls')),
    path('<int:exercise_id>', views.detail, name='detail' ),   
]


