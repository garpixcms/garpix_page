from garpix_page.models import BaseTextDescriptionComponent


class TextDescriptionComponent(BaseTextDescriptionComponent):

    class Meta:
        verbose_name = "Текст+описание"
        verbose_name_plural = "Текст+описание"
        ordering = ('-created_at',)
