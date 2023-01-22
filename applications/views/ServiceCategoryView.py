from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from applications import models, serializers


class ServiceCategoryView(viewsets.ModelViewSet):
    queryset = models.ServiceCategory.objects.all()
    serializer_class = serializers.ServiceCategorySerializer
    permission_classes = [IsAuthenticated]
