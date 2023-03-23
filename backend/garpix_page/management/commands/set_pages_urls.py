from django.core.management.base import BaseCommand

from garpix_page.models import BasePage
from garpix_page.utils.set_children_urls import set_children_url


class Command(BaseCommand):
    help = 'Set old pages urls'

    def handle(self, *args, **options):
        pages = BasePage.objects.all(parent__isnull=True)

        pages_to_update = []

        for page in pages:
            children = page.get_children()

            set_children_url(page, children, pages_to_update)

        BasePage.objects.bulk_update(pages_to_update, ['url'])

        self.stdout.write(self.style.SUCCESS('Done'))
