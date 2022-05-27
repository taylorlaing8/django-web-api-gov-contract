from ..models import UserModel
from rest_framework import generics
from ..serializers import UserSerializer

# from rest_framework_simplejwt.JWTAuthentication import JSONWebTokenAuthentication, IsAuthenticated


class UserCreate(generics.CreateAPIView):
    # API endpoint that allows creation of a new user
    queryset = (UserModel.objects.all(),)
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    # API endpoint that returns a single user by pk.
    # authentication_class = (
    #     JSONWebTokenAuthentication,
    # )  # Don't forget to add a 'comma' after first element to make it a tuple
    # permission_classes = (IsAuthenticated,)
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserUpdate(generics.RetrieveUpdateAPIView):
    # API endpoint that allows a user record to be updated.
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserDelete(generics.RetrieveDestroyAPIView):
    # API endpoint that allows a user record to be deleted.
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserList(generics.ListAPIView):
    # API endpoint that allows user to be viewed.
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
