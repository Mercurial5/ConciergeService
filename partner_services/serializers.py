from rest_framework import serializers

from partner_services import models

from users.serializers import UserOuterSerializer


class PartnerServiceSerializer(serializers.ModelSerializer):
    partner = UserOuterSerializer(read_only=True)

    class Meta:
        model = models.PartnerService
        fields = '__all__'
