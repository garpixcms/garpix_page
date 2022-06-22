from ..models.search_page import SearchPage
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(SearchPage)
class SearchPageAdmin(BasePageAdmin):
    pass
