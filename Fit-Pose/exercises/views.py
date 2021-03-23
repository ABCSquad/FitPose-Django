from django.shortcuts import render
from .models import Exercise
# Create your views here.


#----------------------------- EXERCISE LIST ------------------------------------#

def exercises(request):
    exe = Exercise.objects
    return render(request, 'exercises/allexercises.html',{'exe':exe})