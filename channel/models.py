from django.db import models
from user.models import User
import uuid


def generate_id():
    return str(uuid.uuid4())


# Create your models here.

# Category check performed in front-end
class ChannelCategory(models.Model):
    title = models.CharField(max_length=50)


class OtherLinks(models.Model):
    link = models.CharField(max_length=100)


# Can use ManyToManyField(self) - see Uniback/HL/M2MSelf.PNG
# And can't use ForeignKey as need access to ChannelObj.categories.all()
class FeaturedChannels(models.Model):
    channelid = models.CharField(max_length=40)


class Channel(models.Model):
    _id = models.CharField(
        max_length=40, default=generate_id, unique=True, primary_key=True
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    followers = models.ManyToManyField(User)
    # 1 User can own Many Channels
    # 1 Channel can have 1 owned_by
    owned_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chnl_owned_by"
    )
    categories = models.ManyToManyField(ChannelCategory)
    other_links = models.ManyToManyField(OtherLinks)
    featured_channels = models.ManyToManyField(FeaturedChannels)
    # channel img
    channel_pic_url = models.CharField(
        max_length=400,
        default="https://vtube-test.s3.ap-south-1.amazonaws.com/channel.jpg",
    )
    channel_pic_key = models.CharField(max_length=100, default="channel.jpg")
    # banner img
    channel_banner_url = models.CharField(
        max_length=400,
        default="https://vtube-test.s3.ap-south-1.amazonaws.com/banner1.jpg",
    )
    channel_banner_key = models.CharField(max_length=100, default="banner1.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


# Tip - Make sure related_names don't clash with other models