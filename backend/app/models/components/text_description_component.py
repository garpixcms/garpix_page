from garpix_page.models import BaseTextDescriptionPageComponent


class TextDescriptionPageComponent(BaseTextDescriptionPageComponent):

    class Meta:
        verbose_name = "Текст+описание"
        verbose_name_plural = "Текст+описание"
        ordering = ('-created_at',)
