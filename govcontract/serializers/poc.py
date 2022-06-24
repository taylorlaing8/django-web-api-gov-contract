from numpy import source
from rest_framework import serializers
from ..models import PointOfContact
from .position import PositionSerializer

class PointOfContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=55)
    last_name = serializers.CharField(max_length=55)
    email = serializers.EmailField()
    prefix = serializers.CharField(max_length=10)
    title_id = serializers.IntegerField(write_only=True)    # FOR WRITING POC
    title = PositionSerializer(many=False, read_only=True)  # FOR UPDATING POC

    class Meta:
        model = PointOfContact
        fields = ('__all__')
