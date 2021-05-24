# Generated by Django 3.2 on 2021-05-06 20:19

from django.db import migrations, models
import django.db.models.deletion
import userutils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('channel', '0001_initial'),
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistLikes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes_by', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PlaylistShares',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_by', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='PlayListViews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_by', models.CharField(max_length=40)),
                ('count', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlaylist',
            fields=[
                ('_id', models.CharField(default=userutils.models.generate_id, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('followers', models.ManyToManyField(to='user.User')),
                ('likes', models.ManyToManyField(to='userutils.PlaylistLikes')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_playlist_owner', to='user.user')),
                ('shares', models.ManyToManyField(to='userutils.PlaylistShares')),
                ('videos', models.ManyToManyField(to='video.Video')),
                ('views', models.ManyToManyField(to='userutils.PlayListViews')),
            ],
        ),
        migrations.CreateModel(
            name='ChannelPlaylist',
            fields=[
                ('_id', models.CharField(default=userutils.models.generate_id, max_length=40, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('followers', models.ManyToManyField(to='user.User')),
                ('likes', models.ManyToManyField(to='userutils.PlaylistLikes')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chnl_playlist_owner', to='channel.channel')),
                ('shares', models.ManyToManyField(to='userutils.PlaylistShares')),
                ('videos', models.ManyToManyField(to='video.Video')),
                ('views', models.ManyToManyField(to='userutils.PlayListViews')),
            ],
        ),
    ]
