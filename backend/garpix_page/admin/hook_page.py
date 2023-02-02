from garpix_page.models import HookPage
from django.contrib import admin


@admin.register(HookPage)
class HookPageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sort', )
    list_editable = ('sort',)
