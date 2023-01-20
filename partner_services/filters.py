from django_filters import rest_framework as filters
from partner_services import models


class PartnerServiceFilter(filters.FilterSet):
    # partner = filters.CharFilter(field_name='partner__name', lookup_expr='iexact')

    class Meta:
        model = models.PartnerService
        fields = ['partner', 'service_category']
