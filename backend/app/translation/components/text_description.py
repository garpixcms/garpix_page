from modeltranslation.translator import TranslationOptions, register
from app.models import TextDescriptionComponent


@register(TextDescriptionComponent)
class TextDescriptionComponentTranslationOptions(TranslationOptions):
    fields = ('text', 'description',)
