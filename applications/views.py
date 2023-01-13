from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from applications import serializers, services, exceptions
from users.services import UserService


class ApplicationViewSet(ModelViewSet):
    serializer_class = serializers.ApplicationSerializer
    service = services.ApplicationService(UserService())
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.service.get_list()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            self.service.create(**serializer.validated_data)
        except exceptions.ApplicationException as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
