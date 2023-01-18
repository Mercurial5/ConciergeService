from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications import models

User = get_user_model()


class _CreateFirstApplicationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'city', 'role')


class _CreateFirstApplicationServicesSerializer(serializers.ModelSerializer):
    category = serializers.IntegerField()

    class Meta:
        model = models.Service
        fields = ['category', 'description']


class CreateFirstApplicationSerializer(serializers.ModelSerializer):
    user = _CreateFirstApplicationUserSerializer()
    services = _CreateFirstApplicationServicesSerializer(many=True)

    class Meta:
        model = models.Application
        fields = ('user', 'services')
