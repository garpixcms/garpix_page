from .base_page import BasePage
from django.core.paginator import Paginator


class BaseListPage(BasePage):
    paginate_by = 25
    template = 'garpix_page/default_list.html'

    def get_context(self, request=None, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        object_list = self.children.filter(is_active=True)
        paginator = Paginator(object_list, self.paginate_by)

        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1

        paginated_object_list = paginator.get_page(page)

        context.update({
            'paginator': paginator,
            'paginated_object_list': paginated_object_list,
            'page': page,
        })
        return context

    class Meta:
        abstract = True
