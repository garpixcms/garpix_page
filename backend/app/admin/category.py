from ..models.category import Category
from django.contrib import admin
from garpix_page.admin import BasePageAdmin


@admin.register(Category)
class CategoryAdmin(BasePageAdmin):
    pass
