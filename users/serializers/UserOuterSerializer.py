from rest_framework import serializers
from users import models


class UserOuterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.name')
    city = serializers.CharField(source='city.name')

    class Meta:
        model = models.User
        fields = ['id', 'email', 'name', 'surname', 'role', 'city']
