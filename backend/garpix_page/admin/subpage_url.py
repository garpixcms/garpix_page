from django.contrib.contenttypes.models import ContentType

from garpix_page.models import SubPageUrl
from django.contrib import admin

from garpix_page.utils.get_garpix_page_models import get_garpix_page_models


@admin.register(SubPageUrl)
class SubPageUrlAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'sort', )
    list_editable = ('sort',)
    filter_horizontal = ('page_types',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'page_types' in form.base_fields.keys():
            c_types = [c_type.id for _, c_type in ContentType.objects.get_for_models(*get_garpix_page_models()).items()]
            form.base_fields['page_types'].queryset = ContentType.objects.filter(id__in=c_types)
        return form
