import django_filters
from django_filters import rest_framework as filters, DateFromToRangeFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""
    created_at = DateFromToRangeFilter()
    status = django_filters.CharFilter()
    creator = django_filters.NumberFilter(field_name="creator__id")

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status']
