from modeltranslation.translator import TranslationOptions, register
from ..models import SearchPage


@register(SearchPage)
class SearchPageTranslationOptions(TranslationOptions):
    pass
