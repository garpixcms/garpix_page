from garpix_page.models.components import BaseImagePageComponent


class ImagePageComponent(BaseImagePageComponent):

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображение"
        ordering = ('-created_at',)
