from rest_framework import serializers
from .models import *


class GetVideoTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags

        fields = "__all__"


class GetVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video

        fields = "__all__"


class GetVideoLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes

        fields = "__all__"


class GetVideoDisLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLikes

        fields = "__all__"


class GetVideoCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment

        fields = "__all__"