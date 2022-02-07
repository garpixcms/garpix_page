from garpix_page.models import BaseSliderPageComponent


class SliderPageComponent(BaseSliderPageComponent):

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдер"
        ordering = ('-created_at',)
