from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Position
from ..serializers import PositionSerializer
from rest_framework.permissions import IsAuthenticated


class PositionCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = (Position.objects.all(),)
    serializer_class = PositionSerializer


class PositionDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Position.objects.all().order_by('title')
    serializer_class = PositionSerializer
