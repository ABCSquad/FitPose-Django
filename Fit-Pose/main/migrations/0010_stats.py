# Generated by Django 3.1.2 on 2021-04-14 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20210414_0826'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rep_no', models.DecimalField(decimal_places=1, max_digits=4)),
                ('time', models.DecimalField(decimal_places=1, max_digits=4)),
                ('correct_form', models.DecimalField(decimal_places=1, max_digits=4)),
                ('wrong_form', models.DecimalField(decimal_places=1, max_digits=4)),
                ('session_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.session')),
            ],
        ),
    ]