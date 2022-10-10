from django.template.backends.dummy import TemplateStrings
from garpix_page.settings import TEMPLATE_DIR

__all__ = ('template_source', )


TemplateStrings.app_dirname = TEMPLATE_DIR
template_source = TemplateStrings({'DIRS': [], 'APP_DIRS': True, 'OPTIONS': {}, 'NAME': 'django'})
