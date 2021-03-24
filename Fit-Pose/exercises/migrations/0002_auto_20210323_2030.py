# Generated by Django 3.1.2 on 2021-03-23 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercises',
            name='status',
            field=models.CharField(choices=[('Push', 'Push'), ('Chest', 'Chest'), ('Shoulder', 'Shoulder'), ('Triceps', 'Triceps'), ('Lats', 'Lats'), ('Traps', 'Traps'), ('Biceps ', 'Biceps '), ('Quads', 'Quads'), ('Hamstrings', 'Hamstrings'), ('Glutes', 'Glutes')], default='none', max_length=25),
        ),
        migrations.AlterField(
            model_name='exercises',
            name='title',
            field=models.CharField(max_length=25),
        ),
    ]
