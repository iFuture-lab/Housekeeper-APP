import django_filters
from .models import Housekeeper

class HousekeeperFilter(django_filters.FilterSet):
    # is_available = django_filters.BooleanFilter(field_name='is_available')
    nationality = django_filters.CharFilter(
        field_name='nationality__Nationality', lookup_expr='iexact'
    )
    
    age = django_filters.NumberFilter(
        field_name='Age', 
    )
    
    religion = django_filters.CharFilter(
        field_name='religion__name', lookup_expr='iexact'
    )

    


    class Meta:
        model = Housekeeper
        fields = ['is_available', 'nationality','age','religion']
        
class StatusFilter(django_filters.FilterSet):
    status= django_filters.CharFilter(field_name='status__Status',lookup_expr='iexact')

    class Meta:
        fields = ['status']
