from django.contrib.sites.models import Site


def get_all_sites():
    return Site.objects.all()
