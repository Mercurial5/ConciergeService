from django_filters import rest_framework as filters
from users import models


class UsersFilter(filters.FilterSet):
    # partner = filters.CharFilter(field_name='partner__name', lookup_expr='iexact')
    role = filters.CharFilter(field_name='role__name')

    class Meta:
        model = models.User
        fields = ['role']
