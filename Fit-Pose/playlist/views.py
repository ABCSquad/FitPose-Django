from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist
from exercises.models import Exercise


# Create your views here.


def playlist(request):
    exe = Playlist.objects.filter(user=request.user)
    return render(request, 'playlist/playlist.html',{'exe':exe})
