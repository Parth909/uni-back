from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path("get-usersssss", FilterUser.as_view()),
    path("get-users", GetUsers.as_view()),
    #
    path("create-user", CreateUser.as_view()),
    path("update-user/<str:userid>", UpdateUser.as_view()),
    path("<str:userid>", GetUser.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)