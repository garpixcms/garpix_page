from django.apps import AppConfig
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _


class GarpixPageConfig(AppConfig):
    name = 'garpix_page'
    verbose_name = _('Pages')

    def ready(self):
        from .models.base_page import uncache as page_uncache
        from .models.components.base_component import uncache as component_uncache
        post_save.connect(receiver=page_uncache, sender='garpix_page.BasePage')
        post_save.connect(receiver=component_uncache, sender='garpix_page.BaseComponent')
