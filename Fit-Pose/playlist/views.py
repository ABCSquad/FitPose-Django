from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist
from exercises.models import Exercise
from exercises.models import Exercise, Detail
from exercises.forms import RepsForm
from django.contrib.auth.decorators import login_required

# Create your views here.


def playlist(request):
    user_id = request.user

    if request.method == 'POST':
        exercise_id = get_object_or_404(Exercise, pk=request.POST['exercise_id'])

        # To check if playlist instance exists and add if it doesn't or remove if it does
        instance = Playlist.objects.filter(user=user_id, exercise=exercise_id)
        if instance.exists():
            instance.delete()
        else:
            Playlist(user=user_id, exercise=exercise_id).save()

    
    exe = Playlist.objects.filter(user=request.user)
    return render(request, 'playlist/playlist.html',{'exe':exe})
