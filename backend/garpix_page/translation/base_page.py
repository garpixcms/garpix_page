from modeltranslation.translator import TranslationOptions, register
from ..models import BasePage


@register(BasePage)
class BasePageTranslationOptions(TranslationOptions):
    fields = ('title', 'seo_title', 'seo_keywords', 'seo_description', 'seo_author')
