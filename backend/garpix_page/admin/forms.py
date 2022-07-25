from polymorphic.admin import PolymorphicModelChoiceForm
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class AdminRadioSelectPreview(forms.RadioSelect):
    template_name = 'garpix_page/admin/widgets/radio_preview.html'

    def create_option(self, name, value, *args, **kwargs):
        result = super().create_option(name, value, *args, **kwargs)
        ct = ContentType.objects.filter(pk=value).first()
        result['attrs']['preview'] = None
        if ct is not None:
            model = apps.get_model(ct.app_label, ct.model)
            preview = getattr(model, 'admin_preview_image', None)
            result['attrs']['preview'] = preview
        return result


class PolymorphicModelPreviewChoiceForm(PolymorphicModelChoiceForm):
    type_label = 'Тип'

    ct_id = forms.ChoiceField(
        label=type_label, widget=AdminRadioSelectPreview(attrs={"class": "radiolist"})
    )

    def __init__(self, *args, **kwargs):
        # Allow to easily redefine the label (a commonly expected usecase)
        super().__init__(*args, **kwargs)
        self.fields["ct_id"].label = self.type_label
