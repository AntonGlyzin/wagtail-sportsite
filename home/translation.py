from modeltranslation.translator import register, TranslationOptions
from taggit.models import Tag
from home.models import BlogCategory, CustomMainMenuItem

@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(BlogCategory)
class CatTranslationOptions(TranslationOptions):
    fields = ('name', )

@register(CustomMainMenuItem)
class CatTranslationOptions(TranslationOptions):
    fields = ('link_text', )