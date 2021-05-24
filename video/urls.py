from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path("get-all-tags", GetAllTags.as_view()),
    path("get-all-videos", GetAllVideos.as_view()),
    path("get-all-likes", GetAllVidLikes.as_view()),
    path("get-all-videocomments", GetAllVideoComments.as_view()),
    #
    path("upload-video", UploadVideo.as_view()),
    path("upload-video-info", UploadVideoInfo.as_view()),
    path("update-video-info", UpdateVideoData.as_view()),
    path("update-video-state", UpdateVideoState.as_view()),
    path("add-rmv-vidlike", AddRmvVideoLike.as_view()),
    path("add-rmv-viddislike", AddRmvVideoDislike.as_view()),
    path("add-video-comment", AddVideoComment.as_view()),
    path("rmv-video-comment", RmvVideoComment.as_view()),
    path("user-liked-videos", GetUserLikedVideos.as_view()),
    path("get-user-videos", GetUserVideos.as_view()),
    path("get-recm-videos", GetRecommendedVideos.as_view()),
    path("get-video/<str:videoid>", GetVideo.as_view()),
    path("get-user-vid-likes/<str:userid>", GetUserVidLikes.as_view()),
    path("get-user-vid-dislikes/<str:userid>", GetUserVidDisLikes.as_view()),
    path("incr-video-views", IncrVideoViews.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)