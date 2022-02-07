from django.db import models
from garpix_utils.file import get_file_path

from .base_component import BasePageComponent


class BaseSliderPageComponent(BasePageComponent):
    template = 'garpix_page/components/base_slider.html'

    class Meta:
        abstract = True
