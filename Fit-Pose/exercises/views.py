from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Detail

# Create your views here.


#----------------------------- EXERCISE LIST ------------------------------------#

def exercises(request):
    exe = Exercise.objects
    return render(request, 'exercises/allexercises.html',{'exe':exe})


#----------------------------- DETAILS PAGE ------------------------------------#

max_reps_global = -1

def detail(request, exercise_id):
    if request.method == 'POST':
        global max_reps_global
        max_reps_global = request.POST['max_reps']
        print(max_reps_global)
        return redirect('main:app',detail_id=exercise_id)
    else:
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        details = get_object_or_404(Detail, exercise_id=exercise_id)
        exe = Exercise.objects
        return render(request, 'exercises/detail.html',{'exercise':exercise,'details':details,'exe':exe},) 