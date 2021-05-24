from django.db import models
from user.models import User
from video.models import Video
from channel.models import Channel
import uuid


def generate_id():
    return str(uuid.uuid4())


# Create your models here.

# ________Playlist_________

# No need of foreign key as we don't need to delete the share
class PlaylistShares(models.Model):
    shared_by = models.CharField(max_length=40)


class PlaylistLikes(models.Model):
    likes_by = models.CharField(max_length=40)


class PlayListViews(models.Model):
    viewed_by = models.CharField(max_length=40)
    count = models.IntegerField(default=1)


class ChannelPlaylist(models.Model):
    _id = models.CharField(
        max_length=40, default=generate_id, unique=True, primary_key=True
    )
    owner = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="chnl_playlist_owner"
    )
    title = models.CharField(max_length=100)
    videos = models.ManyToManyField(Video)
    shares = models.ManyToManyField(PlaylistShares)
    likes = models.ManyToManyField(PlaylistLikes)
    views = models.ManyToManyField(PlayListViews)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User)


class UserPlaylist(models.Model):
    _id = models.CharField(
        max_length=40, default=generate_id, unique=True, primary_key=True
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_playlist_owner"
    )
    title = models.CharField(max_length=100)
    videos = models.ManyToManyField(Video)
    shares = models.ManyToManyField(PlaylistShares)
    likes = models.ManyToManyField(PlaylistLikes)
    views = models.ManyToManyField(PlayListViews)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(User)
