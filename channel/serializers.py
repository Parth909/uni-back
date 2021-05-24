from rest_framework import serializers
from .models import Channel, ChannelCategory, FeaturedChannels, OtherLinks

# Helper
class ChannelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelCategory


class GetLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherLinks


# Outgoing
class GetChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel

        fields = "__all__"


class GetChannelCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelCategory

        fields = "__all__"


# Outgoing
class GetUserChannels(serializers.ModelSerializer):
    class Meta:
        model = Channel

        fields = "__all__"


class GetFeatChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeaturedChannels

        fields = "__all__"


# Incoming
# class CreateChannelSerializer(serializers.ModelSerializer):
#     categories = ChannelCategorySerializer(many=True)

#     class Meta:
#         model = Channel

#         fields = (
#             "title",
#             "description",
#             "categories",
#             "channel_pic_url",
#             "channel_pic_key",
#             "channel_banner_url",
#             "channel_banner_key",
#         )


# UpdateChannel without seriaiizer
