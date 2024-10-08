from numpy import source
from rest_framework import serializers
from ..models import Template

class TemplateSerializer(serializers.ModelSerializer):
    title       = serializers.CharField(max_length=256)
    sub_title   = serializers.CharField(max_length=256, allow_null=True)
    data        = serializers.JSONField()

    class Meta:
        model = Template
        fields = ('__all__')
