# Generated by Django 3.1.2 on 2021-03-24 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0004_auto_20210324_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='a_image',
            field=models.ImageField(default='none', upload_to='images/'),
        ),
    ]
