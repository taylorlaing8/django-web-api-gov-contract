from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Template
from ..serializers import TemplateSerializer
from rest_framework.permissions import IsAuthenticated


class TemplateCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = (Template.objects.all(),)
    serializer_class = TemplateSerializer


class TemplateDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer


class TemplateList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Template.objects.all().order_by('title')
    serializer_class = TemplateSerializer
