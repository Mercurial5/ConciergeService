from django_filters import rest_framework as filters
from applications import models


class ApplicationFilter(filters.FilterSet):
    class Meta:
        model = models.Application
        fields = ('owner', 'manager', 'status')
