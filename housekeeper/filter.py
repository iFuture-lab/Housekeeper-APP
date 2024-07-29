import django_filters
from .models import Housekeeper

class HousekeeperFilter(django_filters.FilterSet):
    # is_available = django_filters.BooleanFilter(field_name='is_available')
    nationality = django_filters.CharFilter(
        field_name='nationality__Nationallity', lookup_expr='iexact'
    )

    class Meta:
        model = Housekeeper
        fields = ['is_available', 'nationality','Age']
        
class StatusFilter(django_filters.FilterSet):
    status= django_filters.CharFilter(field_name='status__Status',lookup_expr='iexact')

    class Meta:
        fields = ['status']
