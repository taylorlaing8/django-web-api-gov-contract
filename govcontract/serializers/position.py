from numpy import source
from rest_framework import serializers
from ..models import Position

class PositionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    department = serializers.CharField(max_length=256)

    class Meta:
        model = Position
        fields = ('__all__')
