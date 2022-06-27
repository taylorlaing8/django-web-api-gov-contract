from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Holiday
from ..serializers import HolidaySerializer
from rest_framework.permissions import IsAuthenticated


class HolidayCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = (Holiday.objects.all(),)
    serializer_class = HolidaySerializer


class HolidayDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class HolidayUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class HolidayDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer


class HolidayList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Holiday.objects.all().order_by('date')
    serializer_class = HolidaySerializer
