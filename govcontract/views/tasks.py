from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Task
from ..serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated


class TaskCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = (Task.objects.all(),)
    serializer_class = TaskSerializer


class TaskDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all().order_by('order_id')
    serializer_class = TaskSerializer
