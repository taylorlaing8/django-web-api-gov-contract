from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Contract
from ..serializers import ContractSerializer, ContractListSerializer
from rest_framework.permissions import IsAuthenticated


class ContractCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = (Contract.objects.all(),)
    serializer_class = ContractSerializer


class ContractDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractDelete(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Contract.objects.all().order_by('id')
    serializer_class = ContractListSerializer
