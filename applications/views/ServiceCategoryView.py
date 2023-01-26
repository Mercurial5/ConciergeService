from rest_framework import viewsets

from applications import models, serializers


class ServiceCategoryView(viewsets.ModelViewSet):
    queryset = models.ServiceCategory.objects.all()
    serializer_class = serializers.ServiceCategorySerializer
