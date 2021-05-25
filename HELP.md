### Virtual Environment

##### 1. Creating a virtual environment

```bash
python -m venv your_virtual_env_name
```

### OR

```bash
virtualenv your_venv_name
```

If you want to create virtual environment that contains all the packages that system contains

```bash
virtualenv --system-site-packages your_venv_name
```

##### 2. Activating virtual environment

```bash
your_virtual_env_name/scripts/activate
```

##### 3. Deactivating virtual environment

```bash
deactivate
```

##### 4. After activating ve install the dependencies u want

##### 5. To start django project withour double dirs

Make sure the virtual environment is activated before creating & installing anything
The dot after the project name is important

```bash
django-admin startproject project_name .
```

It will create our mainapp(project) with manage.py outside mainapp like always

#### 6. Creating requirements.txt for vitual environment

Make sure to execute this after activating the virtual environment

```bash
pip freeze > requirements.txt
```

#### 7. If we want to install specific version of a library

```bash
pip install sqlparse==0.4.1
```

#### 8. Installing all libraries from requirements.txt

Use forward slash - if ur in Linux
Use backward slash - if ur in Windows

```bash
pip install -r ./requirements.txt
```

## PIPENV

Make sure you create the pipenv first before doing anything

#### Starting the project

The Pipfile and Pipfile.lock will be created

```bash
pipenv install
```

**If Pipfile already present** - the pipenv install will install the packages in virtual env

Then activate the pipfile

```bash
pipenv shell
```

To check where the virtual env is created again type

```bash
pipenv shell
```

You can see this `Shell for C:\Users\Parth979\.virtualenvs\Pipenv-z9kCMRTG already activated.`

#### Installing & Uninstalling packages

```bash
pipenv install packagename
```

```bash
pipenv uninstall packagename
```

#### To see the packages installed in the virtual env

```bash
pip freeze
```

#### To update the packages

To update all packages

```bash
pipenv update
```

To update specific package

```bash
pipenv update packagename
```

To update specific package with specific version

```bash
pipenv update packagename==2.19.1
```

#### Installing according to requirements.txt

Not at all required when using pipenv, you just need the pipfile & run `pipenv install`

```bash
pip freeze > requirements.txt
```

```bash
pipenv install -r requirements.txt
```

from rest*framework import generics, status
from .serializers import *
from .models import Channel, ChannelCategory
from .serializers import \_
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.db.models.functions import Lower

# user

from user.models import User
from user.serializers import GetUserSerializer

# utils

from operator import itemgetter

# General

class GetChannels(generics.ListAPIView):
queryset = Channel.objects.all()
serializer_class = GetChannelSerializer

class GetAllCats(generics.ListAPIView):
queryset = ChannelCategory.objects.all()
serializer_class = GetChannelCatSerializer

# uncomment it run the server all cats will be delted again comment it

# class DeleteAllCats(generics.DestroyAPIView()):

# queryset = ChannelCategory.objects.all().delete()

# serializer_class = GetChannelCatSerializer

# query set list is normal list

```python
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
            ) = itemgetter(
                "title",
                "description",
                "channel_pic_url",
                "channel_pic_key",
                "channel_banner_url",
                "channel_banner_key",
            )(
                request.data
            )

            # list - even if it contains single categ
            categories, owned_by = itemgetter("categories", "owned_by")(request.data)

            print("________request.data________", request.data)

            # https://stackoverflow.com/questions/7503241/how-to-obtain-a-queryset-of-all-rows-with-specific-fields-for-each-one-of-them
            categories = [cat.capitalize() for cat in categories]

            # flat=True creates query set list of titles
            alpresent_cats = ChannelCategory.objects.filter(
                title__in=categories
            ).values_list("title", flat=True)

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
            cats = matching_cats + npresent_cats
            catobjs = ChannelCategory.objects.filter(title__in=cats)

            if len(catobjs) > 0:
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


class FollowChannel(APIView):
    def patch(self, request, format=None):
        try:
            userid = request.data.get("userid")
            channelid = request.data.get("channelid")

            user = User.objects.filter(_id=userid)[0]
            channel = Channel.objects.filter(_id=channelid)[0]

            owner = GetUserSerializer(channel.owned_by).data

            if user._id == owner["_id"]:
                return JsonResponse(
                    {"error: You cannot follow your own channel"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            print(user not in channel.followers.all())

            return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return JsonResponse(
                {"error": "Data is invalid"}, status=status.HTTP_400_BAD_REQUEST
            )
```

<!-- Validations in /user/<str:userid> -->
<!-- Need to escape double quotes -->
<!-- Remove duplicates in many to many field -->
