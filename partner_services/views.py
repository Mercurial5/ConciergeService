from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from partner_services import serializers, services, exceptions, filters
from users.permissions import IsAdmin, IsManager


class PartnerServicesViewSet(ModelViewSet):
    serializer_class = serializers.PartnerServiceSerializer
    permission_classes = [IsAuthenticated]
    service: services.PartnerServiceServiceInterface = services.PartnerServiceService()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.PartnerServiceFilter

    def get_queryset(self):
        return self.service.list()

    def get_permissions(self):
        permission_classes = self.permission_classes

        if self.request.method == 'POST':
            permission_classes.append(IsAdmin | IsManager)

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.service.create(serializer.validated_data)
        except exceptions.PartnerServiceException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
