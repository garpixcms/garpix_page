from garpix_page.models import BaseSearchPage


class SearchPage(BaseSearchPage):
    paginate_by = 2

    class Meta:
        verbose_name = "Страница поиска"
        verbose_name_plural = "Страница поиска"
        ordering = ('-created_at',)
