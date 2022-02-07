from garpix_page.models import BaseTextPageComponent


class TextPageComponent(BaseTextPageComponent):

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Текст"
        ordering = ('-created_at',)
