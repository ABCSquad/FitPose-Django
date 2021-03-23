from django.db import models

# Create your models here.

class exercises(models.Model):
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/')
    flair = models