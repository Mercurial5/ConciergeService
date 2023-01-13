from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications import models


class _ApplicationUserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'role']


class _ApplicationServicesSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name')

    class Meta:
        model = models.Service
        fields = ['id', 'category', 'description', 'date_from', 'date_to']


class ApplicationSerializer(serializers.ModelSerializer):
    owner = _ApplicationUserSerializer(read_only=True)
    manager = _ApplicationUserSerializer(read_only=True)
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
