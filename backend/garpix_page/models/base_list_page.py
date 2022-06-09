from .base_page import BasePage
from garpix_utils.paginator import GarpixPaginator

from ..pagination import GarpixPagePagination
from ..serializers import get_serializer


class BaseListPage(BasePage):
    paginate_by = 25
    template = 'garpix_page/default_list.html'

    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        object_list = self.children.filter(is_active=True)
        paginator = GarpixPaginator(object_list, self.paginate_by)

        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        paginated_object_list = paginator.get_page(page)

        api_paginator = GarpixPagePagination()

        try:
            model_serializer_class = get_serializer(object_list[0].__class__)

            paginated_children_list = api_paginator.get_paginated_data(queryset=object_list,
                                                                       serializer=model_serializer_class,
                                                                       request=request)
        except Exception:
            paginated_children_list = {
                "count": 0,
                "next": None,
                "prev": None,
                "results": []
            }

        context.update({
            'paginator': paginator,
            'paginated_object_list': paginated_object_list,
            'page': page,
            'paginated_children_list': paginated_children_list
        })
        return context

    class Meta:
        abstract = True
