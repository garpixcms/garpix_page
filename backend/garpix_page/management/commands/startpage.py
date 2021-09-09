from django.core.management.base import BaseCommand
from ...codegenerator import generate_page


class Command(BaseCommand):
    help = 'Start new page. Example: python3 backend/manage.py startpage --app=news --page=category --base=list'

    def add_arguments(self, parser):
        parser.add_argument('--app', type=str)
        parser.add_argument('--page', type=str)
        parser.add_argument('--base', type=str)

    def handle(self, *args, **options):
        app = options['app']
        page = options['page']
        base = options['base']
        generate_page(app, page, base)
        self.stdout.write(self.style.SUCCESS('Done'))
