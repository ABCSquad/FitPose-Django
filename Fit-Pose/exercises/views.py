from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Detail

# Create your views here.


#----------------------------- EXERCISE LIST ------------------------------------#

def exercises(request):
    exe = Exercise.objects
    return render(request, 'exercises/allexercises.html',{'exe':exe})


#----------------------------- DETAILS PAGE ------------------------------------#


def detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, pk=exercise_id)
    details = get_object_or_404(Detail, exercise_id=exercise_id)
    return render(request, 'exercises/detail.html',{'exercise':exercise,'details':details})