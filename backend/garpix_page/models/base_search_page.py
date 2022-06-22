from .base_page import BasePage
from django.db.models import Q
from garpix_utils.paginator import GarpixPaginator


class BaseSearchPage(BasePage):
    paginate_by = 25
    template = 'garpix_page/default_search.html'

    def get_context(self, request=None, *args, **kwargs):
        from ..utils.get_garpix_page_models import get_garpix_page_models
        context = super().get_context(request, *args, **kwargs)
        search_query = request.GET.get('q', None)
        object_list = BasePage.objects.none()

        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        if search_query is not None:
            ids = []
            for Model in get_garpix_page_models():
                q = Q()
                for searchable_field in Model.searchable_fields:
                    searchable_dict = {
                        f'{searchable_field}__icontains': search_query,
                    }
                    q |= Q(**searchable_dict)
                ids += list(Model.on_site.filter(is_active=True).filter(q).values_list('id', flat=True))
            object_list = BasePage.objects.filter(id__in=ids)

        paginator = GarpixPaginator(object_list, self.paginate_by)
        paginated_object_list = paginator.get_page(page)
        context.update({
            'paginator': paginator,
            'paginated_object_list': paginated_object_list,
            'page': page,
            'q': search_query or '',
        })
        return context

    class Meta:
        abstract = True
