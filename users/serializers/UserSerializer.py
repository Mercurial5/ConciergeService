from django.contrib.auth import get_user_model
from rest_framework import serializers

from users import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')
    city = serializers.CharField(source='city.name')

    class Meta:
        model = models.User
        fields = ('id', 'email', 'role', 'city', 'phone', 'created')
