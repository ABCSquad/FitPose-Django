from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist


# Create your views here.


def playlist(request):
    exe = Playlist.objects.filter(user=request.user)
    print(exe.all)
    return render(request, 'playlist/playlist.html',{'exe':exe})