from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class GarpixPageConfig(AppConfig):
    name = 'garpix_page'
    verbose_name = _('Pages')

    def ready(self):
        import garpix_page.signals  # noqa
