from django import forms
from polymorphic.admin import PolymorphicModelChoiceForm
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class AdminRadioSelectPreview(forms.RadioSelect):
    template_name = 'garpix_page/admin/widgets/radio_preview.html'

    def create_option(self, name, value, *args, **kwargs):
        result = super().create_option(name, value, *args, **kwargs)
        ct = ContentType.objects.filter(pk=value).first()
        result['attrs']['preview'] = None
        result['attrs']['group'] = 'Без категории'
        if ct is not None:
            model = apps.get_model(ct.app_label, ct.model)
            preview = getattr(model, 'admin_preview_image', None)
            group = getattr(model, 'admin_group', 'Без категории')
            result['attrs']['preview'] = preview
            result['attrs']['group'] = group
        return result

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["sorted_groups"] = self.sorted_groups(
            context["widget"]["optgroups"]
        )
        context["test"] = self.choices
        return context

    def sorted_groups(self, optgroups):
        groups = optgroups
        result = {}
        for group in groups:
            groupKey = group[1][0]['attrs']['group']
            if groupKey not in result:
                result[groupKey] = []
            result[groupKey].append(*group[1])

        return result

class PolymorphicModelPreviewChoiceForm(PolymorphicModelChoiceForm):
    class Media:
        css = {
            'all': ('css/admin/styles.css',)
        }

    type_label = 'Тип'

    ct_id = forms.ChoiceField(
        label=type_label, widget=AdminRadioSelectPreview(attrs={"class": "radiolist"})
    )

    def __init__(self, *args, **kwargs):
        # Allow to easily redefine the label (a commonly expected usecase)
        super().__init__(*args, **kwargs)
        self.fields["ct_id"].label = self.type_label
