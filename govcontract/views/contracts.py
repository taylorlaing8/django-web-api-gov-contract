from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from ..models import Contract
from ..serializers import ContractSerializer, ContractListSerializer


class ContractCreate(generics.CreateAPIView):
    queryset = (Contract.objects.all(),)
    serializer_class = ContractSerializer


class ContractDetail(generics.RetrieveAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractUpdate(generics.RetrieveUpdateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractDelete(generics.RetrieveDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractList(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractListSerializer
