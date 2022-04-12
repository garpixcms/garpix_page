from modeltranslation.translator import TranslationOptions, register
from garpix_page.models import BaseComponent


@register(BaseComponent)
class BaseComponentTranslationOptions(TranslationOptions):
    fields = ('title', 'text_title')
