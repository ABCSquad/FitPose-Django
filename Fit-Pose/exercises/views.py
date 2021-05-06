from django.shortcuts import render, redirect, get_object_or_404
from .models import Exercise, Detail
from .forms import RepsForm
from playlist.models import Playlist

# Create your views here.


#----------------------------- EXERCISE LIST ------------------------------------#

def exercises(request):

    user_id = request.user

    if request.method == 'POST':
        exercise_id = get_object_or_404(Exercise, pk=request.POST['exercise_id'])

        # To check if playlist instance exists and add if it doesn't or remove if it does
        instance = Playlist.objects.filter(user=user_id, exercise=exercise_id)
        if instance.exists():
            instance.delete()
        else:
            Playlist(user=user_id, exercise=exercise_id).save()

    playlist = Playlist.objects.filter(user=user_id).values('exercise')
    exe = Exercise.objects
    return render(request, 'exercises/allexercises.html',{'exe':exe, 'playlist':playlist})


#----------------------------- DETAILS PAGE ------------------------------------#

max_reps_global = -1

def detail(request, exercise_id):

    if request.method == 'POST':
        form = RepsForm(request.POST)
        if form.is_valid():
            global max_reps_global
            max_reps_global = form.cleaned_data['max_reps']
        return redirect('main:app',detail_id=exercise_id)

    else:
        form = RepsForm()
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        details = get_object_or_404(Detail, exercise_id=exercise_id)
        exe = Exercise.objects
        return render(request, 'exercises/detail.html', {'exercise':exercise,'details':details,'exe':exe,'form':form})

def print_reps():
    global max_reps_global
    return max_reps_global
