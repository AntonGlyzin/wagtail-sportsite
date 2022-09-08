from django.utils.translation import gettext as _
from wagtail.core.blocks import StructBlock, RichTextBlock, StreamBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import (
    CharBlock, ChoiceBlock, RichTextBlock, 
    StreamBlock, StructBlock, TextBlock,
    ChooserBlock
)
from wagtail.embeds.blocks import EmbedBlock

class VideoBlock(StreamBlock):
    class Meta:
        icon = "media"
        label=_(u'Видео')
    video = EmbedBlock(required=True, label=_(u"Видео"), max_width=900)

class CarouselBlock(StructBlock):
    image = ImageChooserBlock(label=_(u"Картинка"))
    class Meta:
        icon = 'image'

class SectionEffectBlock(StructBlock):
    caption = CharBlock(required=True, label=_(u"Заголовок"))
    image = ImageChooserBlock(required=True, label=_(u"Изображение"))
    description = TextBlock(required=True, label=_(u"Описание"))

    class Meta:
        icon = 'fa-solid fa-monitor-waveform'
        

class BaseContentBlock(StreamBlock):
    text = RichTextBlock(
        icon="pilcrow",
        template="blocks/paragraph_block.html",
        label=_(u'Текст')
    )
    image= ImageChooserBlock(
        icon = 'image',
        template = "blocks/image_block.html",
        label=_(u'Изображение')
    )
    video = VideoBlock()
    class Meta:
        icon = "doc-full"
        

