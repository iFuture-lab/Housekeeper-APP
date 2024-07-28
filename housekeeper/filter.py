import django_filters
from .models import Housekeeper

class HousekeeperFilter(django_filters.FilterSet):
    is_available = django_filters.BooleanFilter(field_name='is_available')

    class Meta:
        model = Housekeeper
        fields = ['is_available']
