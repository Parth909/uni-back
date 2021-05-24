from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    # test
    path("get-channels", GetChannels.as_view()),
    path("get-all-cats", GetAllCats.as_view()),
    path("get-all-feats", GetAllFeaturedChannels.as_view()),
    #
    path("create-channel", CreateChannel.as_view()),
    path("update-channel", UpdateChannel.as_view()),
    path("get/<str:channelid>", GetChannel.as_view()),
    path("get-channel-videos", GetChannelVideos.as_view()),
    path("get-featured-channels", GetFeaturedChannels.as_view()),
    path("get-user-channels", GetUserChannels.as_view()),
    path("get-following-channels", GetFollowingChannels.as_view()),
    path("add-rmv-featured-channels", AddRmvFeaturedChannels.as_view()),
    path("foll-unfoll-channel", FollowUnfollowChannel.as_view()),
    path("delete-channel", DeleteChannel.as_view()),
    # danger
    # path("delete-all-links", DeleteAllLinks.as_view()),
    # path("delete-all-cats", DeleteAllCats.as_view()),
    # path("delete-all-channels", DeleteAllChannels.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)