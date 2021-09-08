import logging

from garpix_page.models import BasePage
from garpix_utils.string import get_random_string


class CustomBasePage(BasePage):

    class Meta:
        abstract = True

    def clean(self):
        self._clean_slug()
        super(CustomBasePage, self).clean()

    def _clean_slug(self):
        if self.__class__.on_site.filter(slug=self.slug).exclude(pk=self.pk).exists():
            self.slug = f'{self.slug}{get_random_string(size=4)}'
            message = f'Обнаружен дубль УРЛ для {self.title}. Добавлены символы для уникальности.'
            logging.warning(message)
