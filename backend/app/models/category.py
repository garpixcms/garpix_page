from garpix_page.models import BasePage


class Category(BasePage):
    pass

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"
        ordering = ('-created_at',)
