from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from applications.exceptions import ApplicationException
from applications.serializers import CreateFirstApplicationSerializer, ApplicationCreateSerializer
from applications.services import ApplicationService
from users.serializers import UserCreateSerializer
from users.services import UserService


@api_view(['POST'])
def create_first_application(request):
    serializer = CreateFirstApplicationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data

    user_serializer = UserCreateSerializer(data=serializer.data['user'])
    user_serializer.is_valid(raise_exception=True)

    user_service = UserService()
    user = user_service.create(user_serializer.validated_data)

    data['owner'] = user.pk
    application_serializer = ApplicationCreateSerializer(data=data)
    try:
        application_serializer.is_valid(raise_exception=True)
    except ValidationError as e:
        user_service.delete(user.pk)
        raise ValidationError(e.args)

    application_service = ApplicationService(UserService())
    try:
        application_service.create(application_serializer.validated_data)
    except ApplicationException as e:
        user_service.delete(user.pk)
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({}, status=status.HTTP_201_CREATED)
