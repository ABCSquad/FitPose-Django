#THIS WILL INCLLUDE EXERCISE LIST


from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.exercises, name="exercises"),
]


