from rest_framework.serializers import ModelSerializer

from users.models import Pyment, User


class PymentSerializer(ModelSerializer):
    class Meta:
        model = Pyment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    pyments = PymentSerializer(many=True, read_only=True, source="pyments_user")

    class Meta:
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "phone_number", "sity", "avatar", "pyments")
