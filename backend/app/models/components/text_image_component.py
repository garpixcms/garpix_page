from garpix_page.models import BaseTextImageComponent


class TextImageComponent(BaseTextImageComponent):

    class Meta:
        verbose_name = "Текст+изображение"
        verbose_name_plural = "Текст+изображение"
        ordering = ('-created_at',)
