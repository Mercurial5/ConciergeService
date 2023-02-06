from django.contrib.auth import get_user_model
from djoser.conf import settings
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
        )

    def __init__(self, *args, **kwargs):
        role = kwargs.get('data', dict()).get('role', None)
        if role == 5:  # add logic here for optional viewing
            self.Meta.fields = list(self.Meta.fields)
            self.Meta.fields.append('company_type')
            self.Meta.fields.append('IIN')
            self.Meta.fields.append('code')
        if role == 2:
            self.Meta.fields = list(self.Meta.fields)
            self.Meta.fields.append('specialization')
        super(UserCreateSerializer, self).__init__(*args, **kwargs)
