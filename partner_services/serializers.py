from rest_framework import serializers

from partner_services import models


class PartnerServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PartnerService
        fields = '__all__'
