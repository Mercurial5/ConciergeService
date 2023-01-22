from rest_framework import serializers

from applications import models


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ServiceCategory
        fields = '__all__'
