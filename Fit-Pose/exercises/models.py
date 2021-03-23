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
    image = models.ImageField(upload_to='images/')
    status = models.CharField(default='none', max_length=25, choices=FLAIR_CHOICES)
