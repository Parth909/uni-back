# Generated by Django 3.2 on 2021-05-07 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_visibility',
            field=models.CharField(default='private', max_length=20),
        ),
    ]