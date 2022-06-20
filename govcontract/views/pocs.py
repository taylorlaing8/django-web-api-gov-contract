from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import PointOfContact
from ..serializers import PointOfContactSerializer
from rest_framework.permissions import IsAuthenticated


class PointOfContactCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = (PointOfContact.objects.all(),)
    serializer_class = PointOfContactSerializer


class PointOfContactDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer


class PointOfContactUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer


class PointOfContactDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PointOfContact.objects.all()
    serializer_class = PointOfContactSerializer


class PointOfContactList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = PointOfContact.objects.all().order_by('first_name')
    serializer_class = PointOfContactSerializer
