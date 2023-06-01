from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CoolBeans
from .serializers import AllUsersSerializer, CoolBeansSerializers

User = get_user_model()


# Create your views here.
class AllBeans(generics.ListAPIView):
    """
    First test view
    """

    serializer_class = CoolBeansSerializers
    queryset = CoolBeans.objects.all()


class AllUsers(generics.ListAPIView):
    serializer_class = AllUsersSerializer
    queryset = User.objects.all()
