from django.contrib import admin

from garpix_utils.admin import GarpixSiteConfigurationAdmin
from garpix_page.models.settings import GarpixPageSiteConfiguration


@admin.register(GarpixPageSiteConfiguration)
class GarpixPageSiteConfigurationAdmin(GarpixSiteConfigurationAdmin):
    pass
