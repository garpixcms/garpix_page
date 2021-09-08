from modeltranslation.translator import TranslationOptions, register
from ..models import ListPage


@register(ListPage)
class ListPageTranslationOptions(TranslationOptions):
    pass
