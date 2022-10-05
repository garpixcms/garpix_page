from .base_component import BaseComponent
from garpix_page.fields import GrapesJsHtmlField


class GrapesJsHtmlComponent(BaseComponent):
    html = GrapesJsHtmlField()

    class Meta:
        verbose_name = 'GrapesJs компонент'
        verbose_name_plural = 'GrapesJs компоненты'
