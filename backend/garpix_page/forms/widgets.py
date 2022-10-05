from django import forms
from garpix_page.settings import GRAPESJS_TEMPLATE
from garpix_page.utils import get_render_html_value

__all__ = (
    'GrapesJsWidget',
)


class GrapesJsWidget(forms.Textarea):
    '''
    Textarea form widget with support grapesjs.
    This is widget base config grapesjs.

    '''
    template_name = GRAPESJS_TEMPLATE

    class Media:
        css = {
            'all': (
                'css/grapesjs/grapes.min.css',
                'css/grapesjs/grapesjs-preset-newsletter.css',
                'css/grapesjs/grapesjs-preset-webpage.min.css',
                'css/grapesjs/grapesjs-plugin-filestack.css',
            )
        }
        js = [
            'js/grapesjs/feather-aviary-editor.js',
            'js/grapesjs/grapes.js',
            'js/grapesjs/grapesjs-aviary.min.js',
            'js/grapesjs/grapesjs-preset-newsletter.min.js',
            'js/grapesjs/grapesjs-preset-webpage.min.js',
            'js/grapesjs/grapesjs-lory-slider.min.js',
            'js/grapesjs/grapesjs-tabs.min.js',
            'js/grapesjs/grapesjs-plugin-filestack.min.js',
        ]

    def get_formatted_id_value(self, value_id):
        return value_id.replace('-', '_')

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context['widget']['attrs']['id'] = self.get_formatted_id_value(context['widget']['attrs']['id'])
        context['widget'].update({
            'get_render_html_value': get_render_html_value(
                self.default_html, apply_django_tag=self.apply_django_tag
            ),
            'html_name_init_conf': self.html_name_init_conf,
            'template_choices': self.template_choices,
            'apply_django_tag': int(self.apply_django_tag),
        })

        return context

