from .models import ChannelCategory, OtherLinks, FeaturedChannels
from operator import itemgetter

# Keep the utils seperate so utils can be changed according to change in model


def catsutil(request):
    # list - even if it contains single categ
    categories = itemgetter("categories")(request.data)

    print("________request.data________", request.data)

    categories = [cat.capitalize() for cat in categories]

    # flat=True creates query set list of titles
    alpresent_cats = ChannelCategory.objects.filter(title__in=categories).values_list(
        "title", flat=True
    )

    matching_cats = []
    if len(alpresent_cats) > 0:
        for i in range(len(alpresent_cats)):
            matching_cats.append(alpresent_cats[i])

    npresent_cats = []

    for cat in categories:
        if cat not in alpresent_cats:
            npresent_cats.append(cat)

    # Create Categories if they don't exist
    if len(npresent_cats) > 0:
        catobj_li = [ChannelCategory(title=cat) for cat in npresent_cats]
        ChannelCategory.objects.bulk_create(catobj_li)

    return {"matching_cats": matching_cats, "npresent_cats": npresent_cats}


def otherlinksutil(request):
    # list
    links = itemgetter("other_links")(request.data)

    print("________request.data________", request.data)

    # flat=True creates query set list of links
    alpresent_links = OtherLinks.objects.filter(link__in=links).values_list(
        "link", flat=True
    )

    matching_links = []
    if len(alpresent_links) > 0:
        for i in range(len(alpresent_links)):
            matching_links.append(alpresent_links[i])

    npresent_links = []

    for link in links:
        if link not in alpresent_links:
            npresent_links.append(link)

    # Create Categories if they don't exist
    if len(npresent_links) > 0:
        liobj_li = [OtherLinks(link=link) for link in npresent_links]
        OtherLinks.objects.bulk_create(liobj_li)

    return {"matching_links": matching_links, "npresent_links": npresent_links}


def featuredchnlsutil(request):
    # list
    featchnls = request.data.get("featuredchnlids")

    print("________featchnls________", featchnls)

    if len(featchnls) == 0:
        return {"matching_chnls": [], "npresent_chnls": []}

    # flat=True creates query set list of channelid
    alpresent_chnls = FeaturedChannels.objects.filter(
        channelid__in=featchnls
    ).values_list("channelid", flat=True)

    matching_chnls = []
    if len(alpresent_chnls) > 0:
        for i in range(len(alpresent_chnls)):
            matching_chnls.append(alpresent_chnls[i])

    npresent_chnls = []

    for chnl in featchnls:
        if chnl not in alpresent_chnls:
            npresent_chnls.append(chnl)

    # Create Categories if they don't exist
    if len(npresent_chnls) > 0:
        chobj_li = [FeaturedChannels(channelid=chnl) for chnl in npresent_chnls]
        FeaturedChannels.objects.bulk_create(chobj_li)

    print("______________matching_chnls_________", matching_chnls)
    print("______________npresent_chnls_________", npresent_chnls)

    return {"matching_chnls": matching_chnls, "npresent_chnls": npresent_chnls}