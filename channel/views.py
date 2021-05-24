from rest_framework import generics, status
from .models import Channel, ChannelCategory, OtherLinks
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.db.models.functions import Lower

# user
from user.models import User
from user.serializers import GetUserSerializer

# video
from video.models import Video
from video.serializers import GetVideoSerializer

# utils
from operator import itemgetter
from .utils import *
import json

# General
class GetChannels(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = GetChannelSerializer


class GetAllCats(generics.ListAPIView):
    queryset = ChannelCategory.objects.all()
    serializer_class = GetChannelCatSerializer


class GetAllFeaturedChannels(generics.ListAPIView):
    queryset = FeaturedChannels.objects.all()
    serializer_class = GetFeatChannelSerializer


# uncomment it run the server all cats will be deleted again comment it
# class DeleteAllChannels(generics.DestroyAPIView()):
#     queryset = Channel.objects.all().delete()
#     serializer_class = GetChannelSerializer


# class DeleteAllCats(generics.DestroyAPIView()):
#     queryset = ChannelCategory.objects.all().delete()
#     serializer_class = GetChannelCatSerializer


# class DeleteAllLinks(generics.DestroyAPIView()):
#     queryset = OtherLinks.objects.all().delete()
#     serializer_class = GetLinkSerializer


# query set list is normal list
class CreateChannel(APIView):
    def post(self, request, format=None):
        try:
            (
                title,
                description,
                channel_pic_url,
                channel_pic_key,
                channel_banner_url,
                channel_banner_key,
                owned_by,
            ) = itemgetter(
                "title",
                "description",
                "channel_pic_url",
                "channel_pic_key",
                "channel_banner_url",
                "channel_banner_key",
                "owned_by",
            )(
                request.data
            )

            # Finding the owner
            chnl_owner = User.objects.filter(_id=owned_by)[0]

            chnl = Channel(
                title=title,
                description=description,
                channel_pic_url=channel_pic_url,
                channel_pic_key=channel_pic_key,
                channel_banner_url=channel_banner_url,
                channel_banner_key=channel_banner_key,
                owned_by=chnl_owner,
            )

            chnl.save()

            # Many to many fields added after creating the instance
            matching_cats, npresent_cats = itemgetter("matching_cats", "npresent_cats")(
                catsutil(request)
            )
            cats = matching_cats + npresent_cats

            if len(cats) > 0:
                catobjs = ChannelCategory.objects.filter(title__in=cats)
                chnl.categories.add(*catobjs)

            chnl.save()

            return JsonResponse(
                {"success": "Channel created succcessfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return JsonResponse(
                {"error": "Data is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )


class DeleteChannel(APIView):
    def delete(self, request, format=None):
        usertryingtodel, channelid = itemgetter("usertryingtodel", "channelid")(
            request.data
        )
        print("_______request", request.data)
        user = User.objects.get(_id=usertryingtodel)
        channel = Channel.objects.get(_id=channelid)

        owner = GetUserSerializer(channel.owned_by).data

        if user._id == owner["_id"]:
            channel.delete()
            return JsonResponse(
                {"success": "Deleted the channel successfully"},
                status=status.HTTP_200_OK,
            )
        return JsonResponse(
            {"error": "You don't have permission"}, status=status.HTTP_400_BAD_REQUEST
        )


class FollowUnfollowChannel(APIView):
    def patch(self, request, format=None):
        try:
            userid = request.data.get("userid")
            channelid = request.data.get("channelid")

            user = User.objects.filter(_id=userid)[0]
            channel = Channel.objects.filter(_id=channelid)[0]

            owner = GetUserSerializer(channel.owned_by).data

            if user._id == owner["_id"]:
                return JsonResponse(
                    {"error": "You cannot follow your own channel"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # IMP - I have
            if user not in channel.followers.all():
                channel.followers.add(user)
                channel.save()
                return JsonResponse(
                    {"success": "You are now following this channel"},
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                channel.followers.remove(user)
                channel.save()
                return JsonResponse(
                    {"success": "You unfollowed this channel"},
                    status=status.HTTP_202_ACCEPTED,
                )

            return JsonResponse(
                {"error": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            print("______exception in channel.view.py FollowChannel____")
            return JsonResponse(
                {"error": "Data is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )


class UpdateChannel(APIView):
    def patch(self, request, format=None):
        (
            usertryingtoupdate,  # temporary
            _id,
            title,
            description,
            channel_pic_url,
            channel_pic_key,
            channel_banner_url,
            channel_banner_key,
            owned_by,
        ) = itemgetter(
            "usertryingtoupdate",
            "_id",
            "title",
            "description",
            "channel_pic_url",
            "channel_pic_key",
            "channel_banner_url",
            "channel_banner_key",
            "owned_by",
        )(
            request.data
        )

        chnl_owner = User.objects.filter(_id=owned_by)[0]

        user = User.objects.get(_id=usertryingtoupdate)

        if user._id != chnl_owner._id:
            return JsonResponse(
                {"error": "Forbidden, you don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

        chnl = Channel.objects.filter(_id=_id)[0]

        chnl.title = title
        chnl.description = description
        chnl.channel_pic_url = channel_pic_url
        chnl.channel_pic_key = channel_pic_key
        chnl.channel_banner_url = channel_banner_url
        chnl.channel_banner_key = channel_banner_key
        chnl.owned_by = chnl_owner

        chnl.save()

        # Many to many fields added after creating the instance
        matching_cats, npresent_cats = itemgetter("matching_cats", "npresent_cats")(
            catsutil(request)
        )
        cats = matching_cats + npresent_cats

        if len(cats) > 0:
            catobjs = ChannelCategory.objects.filter(title__in=cats)
            chnl.categories.clear()
            chnl.categories.add(*catobjs)

        matching_links, npresent_links = itemgetter("matching_links", "npresent_links")(
            otherlinksutil(request)
        )
        links = matching_links + npresent_links

        if len(links) > 0:
            olobjs = OtherLinks.objects.filter(link__in=links)
            # clearing out not needed links
            chnl.other_links.clear()
            chnl.other_links.add(*olobjs)

        if len(cats) > 0 or len(links) > 0:
            chnl.save()

        print("__________updated channel_______", chnl)

        # GetChannelSerializer(updatedChnl).data
        return JsonResponse(
            {"success": "Successfully updated the channel"}, status=status.HTTP_200_OK
        )


class GetChannel(APIView):
    def get(self, request, channelid, format=None):
        channel = Channel.objects.get(_id=channelid)

        chnl = GetChannelSerializer(channel).data

        # channel instance has channel.categories.all()

        for i, cat in enumerate(channel.categories.all()):
            chnl["categories"][i] = GetChannelCatSerializer(cat).data

        return JsonResponse(chnl, status=status.HTTP_200_OK)


class AddRmvFeaturedChannels(APIView):
    def patch(self, request, format=None):
        # 29eb5988-12d8-45be-aeb7-f6eb1f73f31a
        # 7a79ddc4-f8d6-4b5b-95aa-3cae75502b20
        userid = request.data.get("usertryingtoup")  # temp
        chnlid = request.data.get("chnlid")
        featuredchnlids = request.data.get("featuredchnlids")
        # list
        usertryingtoup = User.objects.get(_id=userid)
        channeltoUp = Channel.objects.get(_id=chnlid)

        if chnlid in featuredchnlids:
            return JsonResponse(
                {"error": "You can't add your own channel in featured channels"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if usertryingtoup != channeltoUp.owned_by:
            return JsonResponse(
                {"error": "Forbidden, you don't have permission"},
                status=status.HTTP_403_FORBIDDEN,
            )

        matching_chnls, npresent_chnls = itemgetter("matching_chnls", "npresent_chnls")(
            featuredchnlsutil(request)
        )

        chnls = matching_chnls + npresent_chnls
        print("______________chnls", chnls)

        if len(chnls) > 0:

            chobjs = FeaturedChannels.objects.filter(channelid__in=chnls)
            channeltoUp.featured_channels.clear()
            channeltoUp.featured_channels.add(*chobjs)
            channeltoUp.save()

        return JsonResponse(
            {"success": "Added Featured Channels"}, status=status.HTTP_200_OK
        )


class GetChannelVideos(APIView):
    def post(self, request, format=None):
        channelid = request.data.get("channelid")
        channel = Channel.objects.get(_id=channelid)

        videos = Video.objects.filter(owner=channel)
        videos = GetVideoSerializer(videos, many=True).data

        videoli = []

        if len(videos) > 0:
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
                    video["_id"],
                    video["title"],
                    video["thumb_url"],
                    video["video_url"],
                    video["created_at"],
                    video["views"],
                )
                videoli.append(videodict)

        return JsonResponse(videoli, status=status.HTTP_200_OK, safe=False)


class GetFeaturedChannels(APIView):
    def post(self, request, format=None):
        channelid = request.data.get("channelid")

        # 1 Featured Channel Maps to other Channels - like categories
        channel = Channel.objects.get(_id=channelid)

        featchnls = channel.featured_channels.all()
        featchnlids = [chnl.channelid for chnl in featchnls]

        featchnls = Channel.objects.filter(_id__in=featchnlids)
        featchnls = GetChannelSerializer(featchnls, many=True).data

        featli = []
        if len(featchnls) > 0:
            for chnl in featchnls:
                chnldict = {}
                (
                    chnldict["_id"],
                    chnldict["title"],
                    chnldict["followers"],
                    chnldict["channel_pic_url"],
                    chnldict["channel_banner_url"],
                    chnldict["owned_by"],
                ) = (
                    chnl["_id"],
                    chnl["title"],
                    chnl["followers"],
                    chnl["channel_pic_url"],
                    chnl["channel_banner_url"],
                    chnl["owned_by"],
                )
                featli.append(chnldict)

        return JsonResponse(featli, status=status.HTTP_200_OK, safe=False)


class GetUserChannels(APIView):
    def post(self, request, format=None):
        userid = request.data.get("userid")

        user = User.objects.get(_id=userid)

        channels = Channel.objects.filter(owned_by=user)
        channels = GetChannelSerializer(channels, many=True).data

        chnlli = []
        if len(channels) > 0:
            for chnl in channels:
                chnldict = {}

                # ids
                if len(chnl["categories"]) > 0:
                    cats = ChannelCategory.objects.filter(id__in=chnl["categories"])
                    cats = [cat.title for cat in cats]
                    print(cats)
                (
                    chnldict["_id"],
                    chnldict["title"],
                    chnldict["description"],
                    chnldict["followers"],
                    chnldict["channel_pic_url"],
                    chnldict["channel_banner_url"],
                    chnldict["categories"],
                    chnldict["owned_by"],
                ) = (
                    chnl["_id"],
                    chnl["title"],
                    chnl["description"],
                    chnl["followers"],
                    chnl["channel_pic_url"],
                    chnl["channel_banner_url"],
                    cats,
                    chnl["owned_by"],
                )
                chnlli.append(chnldict)

        return JsonResponse(chnlli, status=status.HTTP_200_OK, safe=False)


class GetFollowingChannels(APIView):
    def post(self, request, format=None):
        userid = request.data.get("userid")
        user = User.objects.get(_id=userid)

        channels = Channel.objects.filter(followers=user)

        channels = GetChannelSerializer(channels, many=True).data

        chnlli = []
        if len(channels) > 0:
            for chnl in channels:
                chnldict = {}

                # ids
                if len(chnl["categories"]) > 0:
                    cats = ChannelCategory.objects.filter(id__in=chnl["categories"])
                    cats = [cat.title for cat in cats]
                    print(cats)
                (
                    chnldict["_id"],
                    chnldict["title"],
                    chnldict["description"],
                    chnldict["followers"],
                    chnldict["channel_pic_url"],
                    chnldict["channel_banner_url"],
                    chnldict["categories"],
                    chnldict["owned_by"],
                ) = (
                    chnl["_id"],
                    chnl["title"],
                    chnl["description"],
                    chnl["followers"],
                    chnl["channel_pic_url"],
                    chnl["channel_banner_url"],
                    cats,
                    chnl["owned_by"],
                )
                chnlli.append(chnldict)

        return JsonResponse(chnlli, status=status.HTTP_200_OK, safe=False)