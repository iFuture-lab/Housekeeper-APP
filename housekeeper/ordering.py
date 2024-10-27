from rest_framework import filters
import django_filters
# from django_filters.rest_framework import DjangoFilterBackend

class CustomOrdering(filters.OrderingFilter):

    def get_ordering(self, request, queryset, view):
        sort = request.query_params.get('sort')
        order = request.query_params.get('order', 'ASC') 

        if not sort:
            return None

        if order.upper() == 'DESC':
            sort = f'-{sort}'  # Prefix field with '-' for descending order

        return [sort]
