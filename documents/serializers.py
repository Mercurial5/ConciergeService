from rest_framework import serializers

from documents import models


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DocumentType
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = '__all__'
