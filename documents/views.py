from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from documents import serializer, models, permissions


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializer.DocumentSerializer
    permission_classes = [IsAuthenticated, permissions.IsRelated]
