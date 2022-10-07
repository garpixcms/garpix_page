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
            # 'js/grapesjs/feather-aviary-editor.js',
            'js/grapesjs/grapes.js',
            # 'js/grapesjs/grapesjs-aviary.min.js',
            # 'js/grapesjs/grapesjs-preset-newsletter.min.js',
            # 'js/grapesjs/grapesjs-preset-webpage.min.js',
            # 'js/grapesjs/grapesjs-lory-slider.min.js',
            # 'js/grapesjs/grapesjs-tabs.min.js',
            # 'js/grapesjs/grapesjs-plugin-filestack.min.js',
            'https://unpkg.com/grapesjs-preset-webpage@1.0.2',
            'https://unpkg.com/grapesjs-blocks-basic@1.0.1',
            'https://unpkg.com/grapesjs-plugin-forms@2.0.5',
            'https://unpkg.com/grapesjs-component-countdown@1.0.1',
            'https://unpkg.com/grapesjs-plugin-export@1.0.11',
            'https://unpkg.com/grapesjs-tabs@1.0.6',
            'https://unpkg.com/grapesjs-custom-code@1.0.1',
            'https://unpkg.com/grapesjs-touch@0.1.1',
            'https://unpkg.com/grapesjs-parser-postcss@1.0.1',
            'https://unpkg.com/grapesjs-tooltip@0.1.7',
            'https://unpkg.com/grapesjs-tui-image-editor@0.1.3',
            'https://unpkg.com/grapesjs-typed@1.0.5',
            'https://unpkg.com/grapesjs-style-bg@1.0.5',
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

