from numpy import source
from rest_framework import serializers
from ..models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=256)
    details = serializers.CharField(max_length=256, allow_null=True)
    date = serializers.DateField()
    observed = serializers.DateField()

    class Meta:
        model = Holiday
        fields = ('__all__')
