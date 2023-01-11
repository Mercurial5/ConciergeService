from rest_framework import serializers

from applications import models


class ApplicationSerializer(serializers.ModelSerializer):
    owner = serializers.IntegerField(source='owner.id')
    manager = serializers.IntegerField(source='manager.id')

    class Meta:
        model = models.Application
        fields = '__all__'
