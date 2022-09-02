
def get_seo_value(page, field_name):
    from garpix_page.admin.settings.seo_template import SeoTemplateForm
    from garpix_page.models.settings import SeoTemplate

    seo_templates = SeoTemplate.objects.all()
    for temp in seo_templates:
        if temp.rule_field == SeoTemplateForm.RULE_FIELD.MODEL_NAME and page.__class__.__name__ == temp.model_rule_value or str(
                getattr(page, temp.rule_field, None)) == temp.rule_value:
            return getattr(temp, field_name, '')

    return ''
