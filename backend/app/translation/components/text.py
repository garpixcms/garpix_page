from modeltranslation.translator import TranslationOptions, register
from app.models import TextComponent


@register(TextComponent)
class TextComponentTranslationOptions(TranslationOptions):
    fields = ('text',)
