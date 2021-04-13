from django.db import models
from exercises.models import Detail

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=25,default='none')
    video =  models.ImageField(upload_to='video/',default='none')

    detail = models.ForeignKey(Detail, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title