from django.db import models

# Create your models here.

class Exercise(models.Model):
    FLAIR_CHOICES = (
        ('Push', 'Push'),
        ('Chest', 'Chest'),
        ('Shoulder', 'Shoulder'),
        ('Triceps', 'Triceps'),
        ('Lats', 'Lats'),
        ('Traps', 'Traps'),
        ('Biceps ', 'Biceps '),
        ('Quads', 'Quads'),
        ('Hamstrings', 'Hamstrings'),
        ('Glutes', 'Glutes'),
  
    )

    title = models.CharField(max_length=25)
    image = models.ImageField(upload_to='exercises/')
    flair = models.CharField(default='none', max_length=25, choices=FLAIR_CHOICES)

    def __str__(self):
        return self.title


class Detail(models.Model):
    title = models.CharField(max_length=25,default='none')
    gif_1 =  models.ImageField(upload_to='gifs/',default='none' )
    gif_2 =  models.ImageField(upload_to='gifs/',default='none' )
    step_1 = models.CharField(max_length=200)
    step_2 = models.CharField(max_length=200)
    step_3 = models.CharField(max_length=200)
    step_4 = models.CharField(max_length=200)
    
    exercise = models.ForeignKey(Exercise, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
