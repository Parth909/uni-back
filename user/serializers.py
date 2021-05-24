from rest_framework import serializers
from .models import User

# Meta -
# This is just a class container with some options (metadata) attached to the model. It defines such things as available permissions, associated database table name, whether the model is abstract or not, singular and plural versions of the name etc.

# Outgoing serializer
class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = "__all__"


# Incoming serializer
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ("email", "first_name", "middle_name", "last_name")


# Incoming serializer
class UpdateUserSerializer(serializers.ModelSerializer):

    _id = serializers.CharField(validators=[])
    email = serializers.CharField(validators=[])

    class Meta:
        model = User

        fields = (
            "_id",
            "email",
            "first_name",
            "middle_name",
            "last_name",
            "profile_img_url",
        )
