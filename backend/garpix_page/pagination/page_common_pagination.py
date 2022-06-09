from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination


class GarpixPagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    def get_paginated_data(self, queryset, serializer, request):

        page = self.paginate_queryset(queryset, request)

        if page is not None:
            serializer = serializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return serializer(queryset, many=True).data

    def get_paginated_response(self, data):
        return OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])
