from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import PointOfContact
from ..serializers import PointOfContactSerializer


class PointOfContactCreate(generics.CreateAPIView):
    queryset = (PointOfContact.objects.all(),)
    serializer_class = PointOfContactSerializer


class PointOfContactDetail(generics.RetrieveAPIView):
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer


class PointOfContactUpdate(generics.RetrieveUpdateAPIView):
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer


class PointOfContactDelete(generics.RetrieveDestroyAPIView):
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer


class PointOfContactList(generics.ListAPIView):
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer
