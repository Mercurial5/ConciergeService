from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications import models

from users.serializers import UserOuterSerializer


class _ApplicationServicesSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = models.Service
        fields = ['id', 'category', 'description', 'date_from', 'date_to']


class ApplicationSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='status.name')
    owner = UserOuterSerializer(read_only=True)
    manager = UserOuterSerializer(read_only=True)
    services = _ApplicationServicesSerializer(read_only=True, many=True)

    class Meta:
        model = models.Application
        fields = '__all__'


class _ApplicationServicesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ['category', 'description']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(source='owner_id')
    services = _ApplicationServicesCreateSerializer(many=True)

    class Meta:
        model = models.Application
        fields = '__all__'


class ApplicationPartiallyUpdateSerializer(serializers.ModelSerializer):
    manager = serializers.IntegerField(source='manager_id')

    class Meta:
        model = models.Application
        fields = '__all__'
