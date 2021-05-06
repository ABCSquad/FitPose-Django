from django.db import models
from exercises.models import Exercise
from django.contrib.auth.models import User

# Create your models here.

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)