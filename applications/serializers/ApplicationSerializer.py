from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications import models


class _ApplicationUserField(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'role']


class ApplicationSerializer(serializers.ModelSerializer):
    owner = _ApplicationUserField(read_only=True)
    manager = _ApplicationUserField(read_only=True)

    class Meta:
        model = models.Application
        fields = '__all__'


class ApplicationCreateSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(source='owner_id')

    class Meta:
        model = models.Application
        fields = '__all__'
