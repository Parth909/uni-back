from django.shortcuts import render
from rest_framework import generics, status
from .serializers import *
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from operator import itemgetter

# Create your views here.


class GetUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer


class CreateUser(APIView):
    def post(self, request, format=None):
        # Method 1 - to operate, the data returned is the full object
        serializer = CreateUserSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            email = serializer.data.get("email")
            first_name = serializer.data.get("first_name")
            middle_name = serializer.data.get("middle_name")
            last_name = serializer.data.get("last_name")

            user = User.objects.create(email=email)
            user.first_name = first_name
            user.middle_name = middle_name
            user.last_name = last_name

            user.save()

            return Response(
                GetUserSerializer(user).data, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"Bad Request": "Invalid data..."}, status=status.HTTP_400_BAD_REQUEST
            )


class UpdateUser(APIView):
    def get_object(self, userid):
        try:
            return User.objects.filter(_id=userid)[0]
        except Exception:
            raise Http404

    # Method 2 - to operate but the data returned is limited to data in UpdateUserSerializer
    def put(self, request, userid, format=None):
        user = self.get_object(userid)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                GetUserSerializer(serializer.data).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get(self, request, userid, format=None):

        if len(userid) > 0:
            user = User.objects.get(_id=userid)
            user = GetUserSerializer(user).data

        return JsonResponse({"user": user}, status=status.HTTP_200_OK)


# Test
class FilterUser(APIView):
    def get(self, request, format=None):
        userli = []
        li = [
            "bfe2eb2c-15c1-45af-a726-4f752c8c3ae0",
            "8c09746f-29dd-4c6e-99f9-5c40e0991824",
            "3f779436-69f5-4c74-82b5-909c21b3c120",
        ]
        # Queryset obj returned containing the list of User objs
        users = User.objects.filter(_id__in=li)

        if len(users) > 0:
            for userobj in users:
                # user obj serialized to get us the data
                user = GetUserSerializer(userobj).data
                print("__________user________", user)
                userli.append(user)
        print("__________lenusers_________", len(users))

        return JsonResponse(userli, status=status.HTTP_200_OK, safe=False)

    # request.data - dict of our data
    def post(self, request, format=None):
        email, first_name, middle_name, last_name = itemgetter(
            "email", "first_name", "middle_name", "last_name"
        )(request.data)
        print(
            "______________request.data dict_______________",
            email,
            first_name,
            middle_name,
            last_name,
        )

        return JsonResponse(request.data, status=status.HTTP_200_OK)
