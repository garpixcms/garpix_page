from garpix_page.models.components import BaseImageComponent


class ImageComponent(BaseImageComponent):

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображение"
        ordering = ('-created_at',)
