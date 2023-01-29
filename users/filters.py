from django_filters import rest_framework as filters

from users import models


class UsersFilter(filters.FilterSet):
    class Meta:
        model = models.User
        fields = ['role']
