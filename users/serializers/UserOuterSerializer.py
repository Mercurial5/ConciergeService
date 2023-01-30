from rest_framework import serializers
from users import models


class UserOuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'name', 'surname', 'role', 'city', 'company_name']
