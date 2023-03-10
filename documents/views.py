from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from documents import serializers, models


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = [IsAuthenticated]


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = models.DocumentType.objects.all()
    serializer_class = serializers.DocumentTypeSerializer
    permission_classes = [IsAuthenticated]
