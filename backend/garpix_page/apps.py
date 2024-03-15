from django.apps import AppConfig


class GarpixPageConfig(AppConfig):
    name = 'garpix_page'
    verbose_name = 'Страницы | Pages'

    def ready(self):
        import garpix_page.signals  # noqa
