from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from applications import serializers, services
from users.services import UserService


class ApplicationViewSet(ModelViewSet):
    serializer_class = serializers.ApplicationSerializer
    service = services.ApplicationService(UserService())
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.service.get_list()
