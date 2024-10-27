from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'perPage'
    all = False

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get('all') == 'true':
            self.all = True
            return list(queryset)
        else:
            return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        # print(type(data))
        # if isinstance(data, set):
        if self.all:
            data = list(data)
            return Response({
                'count': len(data),
                'next': None,
                'previous': None,
                'results': data,
            })
        else:
            return super().get_paginated_response(data)

    # def get_paginated_response(self, data):
    #     return super().get_paginated_response(data)
    
    def get_page_size(self, request):
        # print(request.queryset)
        # if request.query_params.get('all') == 'true':
            # print(self.get_count())
            
            # return self.page.paginator.count
        # print(self.page)
        # paginator = self.paginate_queryset(data)
        # all_results = paginator.page(paginator.num_pages).object_list

        return super().get_page_size(request)

    # def paginate_queryset(self, queryset, request, view=None):
    #     if request.query_params.get('all') == 'true':
    #         return queryset
    #     return super().paginate_queryset(queryset, request, view)
        # self.page = super().paginate_queryset(queryset, request, view)
        # return self.page