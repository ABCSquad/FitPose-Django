from django.db import models
from exercises.models import Detail
from django.contrib.auth.models import User

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=25,default='none')
    video =  models.ImageField(upload_to='video/',default='none')

    detail = models.ForeignKey(Detail, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Detail, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, null=False)

class Stats(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    rep_no = models.DecimalField(max_digits=4, decimal_places=1)
    time = models.DecimalField(max_digits=4, decimal_places=1)
    correct_form = models.DecimalField(max_digits=4, decimal_places=1)
    wrong_form = models.DecimalField(max_digits=4, decimal_places=1)