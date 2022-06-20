from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Position
from ..serializers import PositionSerializer


class PositionCreate(generics.CreateAPIView):
    queryset = (Position.objects.all(),)
    serializer_class = PositionSerializer


class PositionDetail(generics.RetrieveAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionUpdate(generics.RetrieveUpdateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDelete(generics.RetrieveDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionList(generics.ListAPIView):
    queryset = Position.objects.all().order_by('title')
    serializer_class = PositionSerializer
