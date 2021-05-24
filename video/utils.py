from .models import *
from channel.serializers import GetChannelSerializer
from operator import itemgetter


def videoutils(request, Model, datatoget, fieldtofilter, capitalize=False):
    utillist = request.data.get(datatoget)

    if len(utillist) == 0:
        return {"matching_tags": [], "npresent_tags": []}

    if capitalize:
        utillist = [item.capitalize() for item in utillist]

    # flat=True creates query set list of titles
    alpresent_items = Model.objects.filter(
        **{f"{fieldtofilter}__in": utillist}
    ).values_list(fieldtofilter, flat=True)

    print("_______________alpresent_items", alpresent_items)

    matching_items = []
    if len(alpresent_items) > 0:
        for i in range(len(alpresent_items)):
            matching_items.append(alpresent_items[i])

    npresent_items = []

    for item in utillist:
        if item not in alpresent_items:
            npresent_items.append(item)

    # Create Categories if they don't exist
    if len(npresent_items) > 0:
        itemobj_li = [Model(**{f"{fieldtofilter}": item}) for item in npresent_items]
        Model.objects.bulk_create(itemobj_li)

    print("_______________matching_items", matching_items)
    print("_______________npresent_items", npresent_items)

    return {"matching_items": matching_items, "npresent_items": npresent_items}


def video_owner(userid, videoid):
    user = User.objects.get(_id=userid)
    video = Video.objects.get(_id=videoid)

    # channel owning the video
    channel = GetChannelSerializer(video.owner).data

    # can't use this after serializing *channel.owned_by* is not a Channel Obj but a simple id
    # owner = GetUserSerializer(channel.owned_by).data

    # User owns -> Channel owns -> Video
    # Only the channel owner can change the video state
    if user._id != channel["owned_by"]:
        return {"allowed": False, "video": video}

    return {"allowed": True, "video": video}
