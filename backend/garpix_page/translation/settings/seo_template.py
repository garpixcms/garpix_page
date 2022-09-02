from modeltranslation.translator import TranslationOptions, register
from garpix_page.models import SeoTemplate


@register(SeoTemplate)
class SeoTemplateTranslationOptions(TranslationOptions):
    fields = ('seo_title', 'seo_keywords', 'seo_description', 'seo_author')
