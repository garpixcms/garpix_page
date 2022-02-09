from garpix_page.models import BaseTextComponent


class TextComponent(BaseTextComponent):

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Текст"
        ordering = ('-created_at',)
