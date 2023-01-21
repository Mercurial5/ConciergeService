from rest_framework import serializers

from documents import models


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = '__all__'
