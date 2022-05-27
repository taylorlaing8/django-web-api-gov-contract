from rest_framework import serializers
from ..models import UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["pk", "first_name", "last_name", "email", "created"]
