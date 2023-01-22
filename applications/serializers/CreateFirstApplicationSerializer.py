from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications import models
from users.serializers import UserCreateSerializer

User = get_user_model()


class _CreateFirstApplicationServicesSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField()
    date_from = serializers.DateField()

    class Meta:
        model = models.Service
        fields = ['category', 'description', 'date_from', 'date_to']


class CreateFirstApplicationSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    services = _CreateFirstApplicationServicesSerializer(many=True)

    class Meta:
        model = models.Application
        fields = ('user', 'services')
