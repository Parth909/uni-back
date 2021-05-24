from django.db import models
import uuid
import random
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver


def generate_id():
    return str(uuid.uuid4())


def generate_profile_url():
    print("generate_proflie_pic has run")
    # -----ENV VARIABLE in prod-----------
    basestr = (
        "https://vtube-test.s3.ap-south-1.amazonaws.com/videos/profile_pics/profile_pic"
    )
    imgstr = str(random.randint(1, 11)) + ".png"
    return basestr + imgstr


# Create your models here.
class User(models.Model):
    # Primary key will also prevent from adding default id
    _id = models.CharField(
        max_length=40, default=generate_id, unique=True, primary_key=True
    )
    email = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bg_theme = models.CharField(max_length=10, default="light")
    profile_img_url = models.CharField(
        max_length=200, default=generate_profile_url, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)