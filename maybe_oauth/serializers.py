from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CoolBeans

User = get_user_model()


class CoolBeansSerializers(serializers.ModelSerializer):
    class Meta:
        model = CoolBeans
        fields = "__all__"


class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
