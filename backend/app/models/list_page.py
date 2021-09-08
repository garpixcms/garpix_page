from garpix_page.models import BaseListPage


class ListPage(BaseListPage):
    paginate_by = 10

    class Meta:
        verbose_name = "Списочная страница"
        verbose_name_plural = "Списочные страницы"
        ordering = ('-created_at',)
