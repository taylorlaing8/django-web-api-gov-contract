from numpy import source
from rest_framework import serializers
from ..models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    details = serializers.CharField(max_length=255, allow_null=True)
    date = serializers.DateTimeField()
    observed = serializers.DateTimeField()

    class Meta:
        model = Holiday
        fields = ('__all__')
