from ..models.list_page import ListPage
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(ListPage)
class ListPageAdmin(BasePageAdmin):
    pass
