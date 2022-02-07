from garpix_page.models import BaseTextImagePageComponent


class TextImagePageComponent(BaseTextImagePageComponent):

    class Meta:
        verbose_name = "Текст+изображение"
        verbose_name_plural = "Текст+изображение"
        ordering = ('-created_at',)
