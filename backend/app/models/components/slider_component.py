from garpix_page.models import BaseSliderComponent


class SliderComponent(BaseSliderComponent):

    class Meta:
        verbose_name = "Слайдер"
        verbose_name_plural = "Слайдер"
        ordering = ('-created_at',)
