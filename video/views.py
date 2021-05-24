from rest_framework import generics, status
from rest_framework.views import APIView
from django.http import JsonResponse
from django.db import transaction
from operator import itemgetter
from django.contrib.humanize.templatetags.humanize import (
    naturaltime,
    naturalday,
    intword,
)
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .serializers import *
from .utils import *

# from .datetimeutil import naturaltime

from channel.models import Channel
from channel.serializers import GetChannelSerializer
from user.models import User
from user.serializers import GetUserSerializer

# danger
# class GetAllVideos(generics.DestroyAPIView()):
#     queryset = Video.objects.all().delete()
#     serializer_class = GetVideoSerializer


# class GetAllLikes(generics.DestroyAPIView()):
#     queryset = Likes.objects.all().delete()
#     serializer_class = GetVideoLikesSerializer


# generics
class GetAllTags(generics.ListAPIView):
    queryset = Tags.objects.all()
    serializer_class = GetVideoTagSerializer


class GetAllVideos(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = GetVideoSerializer


class GetAllVidLikes(generics.ListAPIView):
    queryset = Likes.objects.all()
    serializer_class = GetVideoLikesSerializer


class GetAllVideoComments(generics.ListAPIView):
    queryset = VideoComment.objects.all()
    serializer_class = GetVideoCommentSerializer


# Create your views here.
class UploadVideo(APIView):
    def post(self, request, format=None):
        pass


class UploadVideoInfo(APIView):
    def post(self, request, format=None):
        title, desc, thumb_url, thumb_key = itemgetter(
            "title", "desc", "thumb_url", "thumb_key"
        )(request.data)

        # temp
        userid, channelid, video_tags, video_url, video_key = itemgetter(
            "userid", "channelid", "video_tags", "video_url", "video_key"
        )(request.data)

        user = User.objects.get(_id=userid)
        channel = Channel.objects.get(_id=channelid)

        owner = GetUserSerializer(channel.owned_by).data

        if user._id != owner["_id"]:
            return JsonResponse(
                {"error": "Forbidden, you don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

        video = Video(
            title=title,
            description=desc,
            thumb_url=thumb_url,
            thumb_key=thumb_key,
            video_url=video_url,  # temp - later patch it
            video_key=video_key,  # temp
            owner=channel,
        )

        video.save()

        matching_items, npresent_items = itemgetter("matching_items", "npresent_items")(
            videoutils(
                request=request,
                Model=Tags,
                datatoget="video_tags",
                fieldtofilter="name",
                capitalize=True,
            )
        )

        tags = matching_items + npresent_items

        video.uploaded_by.add(channel)

        if len(tags) > 0:
            tagobjs = Tags.objects.filter(name__in=tags)
            # no to clear tags while creating
            video.tags.add(*tagobjs)

        video.save()

        return JsonResponse(
            {"success": "Video info uploaded successfully"}, status=status.HTTP_200_OK
        )


class UpdateVideoData(APIView):
    def patch(self, request, format=None):
        userid, videoid, video_tags, thumb_url, thumb_key = itemgetter(
            "userid", "videoid", "video_tags", "thumb_url", "thumb_key"
        )(request.data)

        allowed, video = itemgetter("allowed", "video")(
            video_owner(userid=userid, videoid=videoid)
        )

        if not allowed:
            return JsonResponse(
                {"error": "You don't have permission"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # thumbnail can't be empty
        video.thumb_url = thumb_url
        video.thumb_key = thumb_key

        if len(video_tags) > 0:
            matching_items, npresent_items = itemgetter(
                "matching_items", "npresent_items"
            )(
                videoutils(
                    request=request,
                    Model=Tags,
                    datatoget="video_tags",
                    fieldtofilter="name",
                    capitalize=True,
                )
            )

            print("___matching____", matching_items)
            print("___npresent___", npresent_items)

            tags = matching_items + npresent_items

            if len(tags) > 0:
                tagobjs = Tags.objects.filter(name__in=tags)
                video.tags.clear()  # clear all before adding
                video.tags.add(*tagobjs)

        video.save()

        return JsonResponse(
            {"success": "Video Updated Successfully"}, status=status.HTTP_200_OK
        )


class UpdateVideoState(APIView):
    def patch(self, request, format=None):
        userid, videoid, video_visibility = itemgetter(
            "userid", "videoid", "video_status"
        )(request.data)

        allowed, video = itemgetter("allowed", "video")(
            video_owner(userid=userid, videoid=videoid)
        )

        if not allowed:
            return JsonResponse(
                {"error": "You don't have permission"}, status=status.HTTP_200_OK
            )

        valid = ["public", "private", "custom"]

        if video_visibility not in valid:
            return JsonResponse(
                {"error": "Video State not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        video.video_visibility = video_visibility

        video.save(update_fields=["video_visibility"])

        return JsonResponse(
            {"success": "Updated Video State"}, status=status.HTTP_200_OK
        )


class AddRmvVideoLike(APIView):
    def patch(self, request, format=None):
        userid, videoid = itemgetter("userid", "videoid")(request.data)

        user = User.objects.get(_id=userid)
        video = Video.objects.get(_id=videoid)

        # channel owning the video
        channel = GetChannelSerializer(video.owner).data

        # creating new like
        liked = Likes.objects.filter(liked_by=user._id)

        if len(liked) == 0:
            likeobj = Likes(liked_by=user._id)
            likeobj.save()
            like = likeobj
        else:
            like = liked[0]

        # before adding in likes check if dislike exists
        disliked = DisLikes.objects.filter(disliked_by=user._id)

        if len(disliked) > 0:
            video.dislikes.remove(disliked[0])
            # video.save()

        # IMP - **added** & **removed** are keywords on the basis of them Redux State will be updated
        if like not in video.likes.all():
            video.likes.add(like)
            video.save()
            return JsonResponse(
                {"success": "added to Liked Videos"}, status=status.HTTP_200_OK
            )
        else:
            video.likes.remove(like)
            video.save()
            return JsonResponse(
                {"success": "removed from Liked Videos"}, status=status.HTTP_200_OK
            )

        return JsonResponse(
            {"success": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST
        )


class AddRmvVideoDislike(APIView):
    def patch(self, request, format=None):
        userid, videoid = itemgetter("userid", "videoid")(request.data)

        user = User.objects.get(_id=userid)
        video = Video.objects.get(_id=videoid)

        # channel owning the video
        channel = GetChannelSerializer(video.owner).data

        # creating new like
        disliked = DisLikes.objects.filter(disliked_by=user._id)

        if len(disliked) == 0:
            dislikeobj = DisLikes(disliked_by=user._id)
            dislikeobj.save()
            dislike = dislikeobj
        else:
            dislike = disliked[0]

        # before adding in dislikes check if like exists
        liked = Likes.objects.filter(liked_by=user._id)

        if len(liked) > 0:
            video.likes.remove(liked[0])
            # video.save()

        # IMP - **added** & **removed** are keywords on the basis of them Redux State will be updated
        if dislike not in video.dislikes.all():
            video.dislikes.add(dislike)
            video.save()
            return JsonResponse(
                {"success": "added to disliked videos"}, status=status.HTTP_200_OK
            )
        else:
            video.dislikes.remove(dislike)
            video.save()
            return JsonResponse(
                {"success": "removed from disliked videos"}, status=status.HTTP_200_OK
            )

        return JsonResponse(
            {"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST
        )


class AddVideoComment(APIView):
    def post(self, request, format=None):
        userid = request.data.get("userid")
        videoid = request.data.get("videoid")
        commentdesc = request.data.get("commentdesc")

        user = User.objects.get(_id=userid)
        video = Video.objects.get(_id=videoid)

        # Here for every comment we need a Obj not like *Like or Dislike*
        videocomment = VideoComment(comment_owner=user, comment_description=commentdesc)

        videocomment.save()

        video.comments.add(videocomment)

        video.save()

        return JsonResponse({"success": "Comment added"}, status=status.HTTP_200_OK)


class RmvVideoComment(APIView):
    def post(self, request, format=None):
        userid = request.data.get("userid")
        videoid = request.data.get("videoid")
        commentid = request.data.get("commentid")

        user = User.objects.get(_id=userid)
        video = Video.objects.get(_id=videoid)
        comment = VideoComment.objects.get(id=commentid)
        # serializing will convert comment.comment_owner User obj to String
        serzcomment = GetVideoCommentSerializer(comment).data

        if user._id != serzcomment["comment_owner"]:
            return JsonResponse(
                {"error": "You don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if comment in video.comments.all():
            video.comments.remove(comment)
            video.save()
            comment.delete()
            return JsonResponse(
                {"success": "Comment Deleted"}, status=status.HTTP_200_OK
            )

        return JsonResponse(
            {"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST
        )


class GetUserLikedVideos(APIView):
    def post(self, request, format=None):

        userid = request.data.get("userid")

        # seeing access of Videos from Likes

        like = Likes.objects.filter(liked_by=userid)

        if len(like) == 0:
            return JsonResponse(
                {"msg": "You have no liked videos"}, status=status.HTTP_200_OK
            )
        like = like[0]
        # print(Video._meta.model_name) - m2mfield.modelname_set.all()
        print(like.video_set.all())

        videoli = []
        video_set = like.video_set.all()

        if len(video_set) > 0:
            for video in video_set:
                _id, title, owner, thumb_url, thumb_key = itemgetter(
                    "_id", "title", "owner", "thumb_url", "thumb_key"
                )(GetVideoSerializer(video).data)
                # After serializing everything bcmz a string, dict & list

                # these methods need datetime obj
                print("_____naturalday_____", naturaltime(video.created_at))

                chnldata = {
                    "_id": _id,
                    "title": title,
                    "owner": owner,
                    "created_at": naturaltime(video.created_at),
                    "thumb_url": thumb_url,
                    "thumb_key": thumb_key,
                }
                videoli.append(chnldata)

        return JsonResponse(videoli, status=status.HTTP_200_OK, safe=False)


class GetUserVidLikes(APIView):
    def get(self, request, userid, format=None):

        like = Likes.objects.filter(liked_by=userid)
        vidlikes = []

        if len(like) > 0:
            like = like[0]
        else:
            return JsonResponse({"vidlikes": vidlikes}, status=status.HTTP_200_OK)

        if len(like.video_set.all()) > 0:
            for video in like.video_set.all():
                vidlikes.append(video._id)

        return JsonResponse({"vidlikes": vidlikes}, status=status.HTTP_200_OK)


class GetUserVidDisLikes(APIView):
    def get(self, request, userid, format=None):

        dislike = DisLikes.objects.filter(disliked_by=userid)
        viddislikes = []

        if len(dislike) > 0:
            dislike = dislike[0]
        else:
            return JsonResponse({"viddislikes": viddislikes}, status=status.HTTP_200_OK)

        if len(dislike.video_set.all()) > 0:
            for video in dislike.video_set.all():
                viddislikes.append(video._id)

        return JsonResponse({"viddislikes": viddislikes}, status=status.HTTP_200_OK)


class GetUserVideos(APIView):
    def post(self, request, format=None):
        userid = request.data.get("userid")

        user = User.objects.get(_id=userid)
        videos = Video.objects.all()

        videoli = []
        for video in videos:
            videodict = {}
            (
                videodict["_id"],
                videodict["title"],
                videodict["thumb_url"],
                videodict["video_url"],
                videodict["created_at"],
                videodict["views"],
            ) = (
                video._id,
                video.title,
                video.thumb_url,
                video.video_url,
                video.created_at,
                video.views,
            )
            videodict["channel_title"], videodict["channel_pic_url"] = itemgetter(
                "title", "channel_pic_url"
            )(GetChannelSerializer(video.owner).data)
            videoli.append(videodict)

        return JsonResponse(videoli, status=status.HTTP_200_OK, safe=False)


class GetRecommendedVideos(APIView):
    def post(self, request, format=None):
        userid = request.data.get("userid")
        current_video_id = request.data.get("current_video_id")

        # .filter()
        videos = Video.objects.exclude(_id=current_video_id).all()

        videos = GetVideoSerializer(videos, many=True).data
        owners = [video["owner"] for video in videos]
        print(owners)
        owners = GetChannelSerializer(
            Channel.objects.filter(_id__in=owners), many=True
        ).data
        owners = [dict(owner) for owner in owners]

        # Can afford to perform computation but can't afford to hit db everytime
        for video in videos:
            # will return the first match & won't keep on iterating
            video["owner"] = next(
                (channel for channel in owners if channel["_id"] == video["owner"]),
                None,
            )

        return JsonResponse({"videos": videos}, status=status.HTTP_200_OK)


class GetVideo(APIView):
    def get(self, request, videoid, format=None):

        video = Video.objects.get(_id=videoid)

        video_tags = GetVideoTagSerializer(video.tags.all(), many=True).data
        video_tags = [dict(od) for od in video_tags]

        video_comments = GetVideoCommentSerializer(
            video.comments.all()[:10], many=True
        ).data
        video_comments = [dict(od) for od in video_comments]
        user_ids = [comment["comment_owner"] for comment in video_comments]

        if len(video_comments) > 0:
            comment_owners = GetUserSerializer(
                User.objects.filter(_id__in=user_ids), many=True
            ).data
            users = [dict(user) for user in comment_owners]
            for comment in video_comments:
                comment["comment_owner"] = next(
                    (user for user in users if user["_id"] == comment["comment_owner"]),
                    None,
                )

        video_owner = GetChannelSerializer(video.owner).data
        video_owner["followers"] = intword(len(video_owner["followers"]))

        likes = GetVideoLikesSerializer(video.likes.all(), many=True).data
        likes = [od["liked_by"] for od in likes]
        dislikes = GetVideoDisLikesSerializer(video.dislikes.all(), many=True).data
        dislikes = [od["disliked_by"] for od in dislikes]

        video = GetVideoSerializer(video).data

        video["tags"] = video_tags
        video["comments"] = video_comments
        video["owner"] = video_owner
        video["likes"] = likes
        video["dislikes"] = dislikes

        return JsonResponse(video, status=status.HTTP_200_OK)


class IncrVideoViews(APIView):
    def patch(self, request, format=None):
        videoid = request.data.get("videoid")

        video = Video.objects.get(_id=videoid)

        video.views += 1

        # update_fields won't update the auto_now field unless mention explicitly in update_fields
        video.save()

        return JsonResponse({"views": video.views}, status=status.HTTP_200_OK)


# PtToNote :-  can't use update_fields on m2m fields
