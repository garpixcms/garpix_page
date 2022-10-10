from .base_component import BaseComponent
from garpix_page.fields import GrapesJsHtmlField
from django.conf import settings

MEDIA_URL = settings.MEDIA_URL


class GrapesJsHtmlComponent(BaseComponent):
    html = GrapesJsHtmlField()
    admin_preview_image = 'garpix_page/images/admin/grapesjs.png'

    def get_context(self, request):
        context = super().get_context(request)
        context.update({
            'css': request.build_absolute_uri(f'{MEDIA_URL}grapesjs/html_{self.pk}_css.css'),
            'js': request.build_absolute_uri(f'{MEDIA_URL}grapesjs/html_{self.pk}_js.js')
        })
        return context

    class Meta:
        verbose_name = 'GrapesJs компонент'
        verbose_name_plural = 'GrapesJs компоненты'
