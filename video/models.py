from django.db import models
from user.models import User
from channel.models import Channel
import uuid


def generate_id():
    return str(uuid.uuid4())


# Create your models here.


class Tags(models.Model):
    name = models.CharField(max_length=30)


class Likes(models.Model):
    # User id in string format
    liked_by = models.CharField(max_length=40)


class DisLikes(models.Model):
    # User id in string format
    disliked_by = models.CharField(max_length=40)


class Shares(models.Model):
    # User id in string format
    shared_by = models.CharField(max_length=40)


# Many comments belong to 1 user
class VideoComment(models.Model):
    #  Many USERS will be the *comment_owner* of VidComment - this is not True but we need the Cascade effect + we can match comment_owner with Userobj while filtering
    comment_owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_owner"
    )
    comment_description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Video(models.Model):
    _id = models.CharField(
        max_length=40, default=generate_id, unique=True, primary_key=True
    )
    # Many Channels are *owner* of 1 video - this is not true but need this CASCADE effect + we can match owner with channelObj while filtering
    owner = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="video_owned_by"
    )
    # taking advntg of this later
    uploaded_by = models.ManyToManyField(Channel)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tags)
    likes = models.ManyToManyField(Likes)
    dislikes = models.ManyToManyField(DisLikes)
    shares = models.ManyToManyField(Shares)
    video_visibility = models.CharField(max_length=20, default="private")
    # thumbnail img
    thumb_url = models.CharField(max_length=400)
    thumb_key = models.CharField(max_length=100)
    # video
    video_url = models.CharField(max_length=400)
    video_key = models.CharField(max_length=100)
    # comment
    comments = models.ManyToManyField(VideoComment)
