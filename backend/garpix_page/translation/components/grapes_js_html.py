from modeltranslation.translator import TranslationOptions, register
from garpix_page.models import GrapesJsHtmlComponent


@register(GrapesJsHtmlComponent)
class GrapesJsHtmlComponentTranslationOptions(TranslationOptions):
    pass
