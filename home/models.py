from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from django import forms
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (FieldPanel, 
                                InlinePanel, 
                                MultiFieldPanel, 
                                StreamFieldPanel,
                                PageChooserPanel,
                                HelpPanel)
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel 
from django.utils.translation import gettext_lazy as _
from home.blocks import (CarouselBlock, BaseContentBlock,
                     SectionEffectBlock, VideoBlock)
from wagtail.snippets.blocks import SnippetChooserBlock
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from django_extensions.db.fields import AutoSlugField
from wagtailcaptcha.models import WagtailCaptchaForm
from wagtail.contrib.forms.models import AbstractFormField, AbstractForm
from django_comments_xtd.models import XtdComment
from django.shortcuts import get_object_or_404
from taggit.models import Tag
from wagtailmenus.models import AbstractMainMenuItem
from wagtailseo.models import SeoMixin
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList
from typing import Optional, Iterable
import os
from wagtail.images.views.serve import generate_image_url
import base64
from wagtail.api import APIField
from django.core.files.storage import Storage
from django.utils.html import format_html
from wagtail.admin.ui.components import Component

class RenderImgBase64Panel(Component):
    def render_html(self, parent_context):
        return format_html("<h1></h1>", "Welcome to my app!")
PanelBase64 = RenderImgBase64Panel()

def convert_symbol(string):
    exclude_symbol = [
        ' ', '<', '>', '#', '%',
        '"', '|', '^', '[', ']', '`',
        ';', ':', '?', '@', '&', '=',
        '+', '$', ',', '/', '\\', '!'
    ]
    new_string = ''
    for item in string.lower().strip():
        if item in exclude_symbol:
            new_string += '-'
        else:
            new_string += item
    return new_string

class HomePage(SeoMixin, Page):
    subpage_types = ['BlogIndexPage', 'IndexProgram', 'ContactPage']
    carousel_block = models.ForeignKey(
        'home.CarouselGeneral',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(u'Карусель')
    )
    section_program = ParentalKey('home.IndexProgram', 
                                on_delete=models.SET_NULL,
                                blank=True, null=True,
                                verbose_name=_(u'Список программ'))

    head_effects = models.CharField(verbose_name=_(u'Заголовок'), max_length=255, blank=True)
    effects_sport = StreamField([
        ('effects_sport', SectionEffectBlock(label=_(u'Элемент')))
    ], blank=True, verbose_name=_(u'Польза спорта')) 


    head_testimonial = models.CharField(verbose_name=_(u'Заголовок'), max_length=255, blank=True)
    list_testimonial_sport = StreamField([
        ('testimonial_sport', SnippetChooserBlock('home.TestimonialSport', label=_(u'Цитата')))
    ], blank=True, verbose_name=_(u'Цитата'))                        

    content_panels = Page.content_panels + [
        SnippetChooserPanel('carousel_block'),
        FieldPanel('section_program'),
        MultiFieldPanel([
            FieldPanel('head_effects'),
            StreamFieldPanel('effects_sport')
        ], heading=_(u'Полезные свойства')),
        MultiFieldPanel([
            FieldPanel('head_testimonial'),
            SnippetChooserPanel('list_testimonial_sport')
        ], heading=_(u'Рекомендации'))
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading=_('Content')),
        ObjectList(Page.promote_panels, heading=_('Promote')),
        ObjectList(Page.settings_panels, heading=_('Settings'), classname="settings"),

        ObjectList(SeoMixin.seo_panels, heading="SEO", classname="seo"),
    ])

@register_snippet
class CarouselGeneral(models.Model):
    text = models.CharField(max_length=255, verbose_name=_(u'Заголовок'))
    main_content = StreamField([
        ('carousel', CarouselBlock(label=_(u'Элемент карусели')))
    ], blank=True, verbose_name=_(u'Контент для карусели'))

    panels = [
        FieldPanel('text'),
        StreamFieldPanel('main_content')
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = _(u'Карусель для сайта')
        verbose_name = _(u'элемент')


@register_snippet
class TestimonialSport(models.Model):
    author = models.CharField(max_length=255, verbose_name=_(u'Автор'))
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(u'Изображение')
    )
    text = models.TextField(verbose_name=_(u'Цитата'))
    panels = [
        FieldPanel('author'),
        ImageChooserPanel('image'),
        FieldPanel('text')
    ]

    def __str__(self):
        return self.author

    class Meta:
        verbose_name_plural = _(u'Цитаты про спорт')
        verbose_name = _(u'цитату')


class IndexProgram(Page):
    parent_page_types = ['HomePage']
    subpage_types = ['PageProgram']
    template = 'home/page_list_sport.html'
    
    head_text = models.CharField(verbose_name=_(u'Текст для секции'),
                                max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('head_text'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        pages = self.get_pages()
        context['pages'] = self.paginate(request, pages)
        return context
    
    def get_pages(self):
        pages = self.get_children().live().order_by('-first_published_at')
        return pages

    def paginate(self, request, *args):
        page = request.GET.get('page')
        count_posts = SiteSettings.objects.first().count_posts
        paginator = Paginator(self.get_pages(), count_posts)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    def get_programs_carusel(self):
        list_prog = []
        sub_list = []
        progs = self.get_children().live().order_by('-first_published_at')
        for i, prog in enumerate(progs, 1):
            sub_list.append(prog)
            if i%3 == 0 or i == progs.count():
                list_prog.append(sub_list)
                sub_list = []
        return list_prog

    def get_absolute_url(self):
        return self.get_url()

    class Meta:
        verbose_name = _(u'Программы')


class PageProgram(Page):
    parent_page_types = ['IndexProgram']
    subpage_types = []
    template = 'home/page_sport.html'

    intro = RichTextField(
        features=['h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul'],
        verbose_name=_(u'Предпросмотр'), blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(u'Изображение')
    )

    content = StreamField([
        ('content', BaseContentBlock(label=_(u'Контент')))
        
    ], verbose_name=_(u'Контент'))

    date_created = models.DateField(verbose_name=_(u'Дата'), default=date.today)

    price = models.CharField(verbose_name=_(u'Цена программы'), max_length=10, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('title'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('image'),
        StreamFieldPanel('content'),
        FieldPanel('price'),
        FieldPanel('date_created'),
    ]

    def get_absolute_url(self):
        return self.get_url()

    class Meta:
        verbose_name_plural = _(u'Программы')
        verbose_name = _(u'Программа')



@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_(u'Категория'))
    slug = AutoSlugField(populate_from="name", 
                        editable=True, 
                        verbose_name=_('Слаг'), 
                        help_text=_(u'Заполняется автоматически при сохранение, когда поле пустое.'))

    def slugify_function(self, content):
        return convert_symbol(content)

    def get_absolute_url(self):
        return f'/блог/категория/{self.slug}/'

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = _(u'Список категорий')
        verbose_name = _(u'категорию')

    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'home.BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogIndexPage(RoutablePageMixin, Page):
    parent_page_types = ['HomePage']
    subpage_types = ['BlogPage']
    template = 'home/page_list_sport.html'

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['pages'] = self.get_pages(request=request)
        return context
    
    def get_pages(self, **kwargs):
        pages = BlogPage.objects.live().descendant_of(self)
        tag = kwargs.get('tag')
        cat = kwargs.get('cat')
        if tag:
            pages = pages.filter(tags__slug__in=[tag])
        elif cat:
            pages = pages.filter(categories__slug__in=[cat])
        pages = pages.order_by('-first_published_at')
        request = kwargs.get('request')
        return self.paginate(request, pages)

    def paginate(self, request, pages):
        page = request.GET.get('page')
        count_posts = SiteSettings.objects.first().count_posts
        paginator = Paginator(pages, count_posts)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)
        return pages

    @route(r'^теги/(?P<tag>[\w-]+)/$', name='tag_archive')
    def tag_archive(self, request, tag=None):
        obj_tag = get_object_or_404(Tag, slug=tag)
        posts = self.get_pages(request=request, tag=tag)
        context = {
            'tag': obj_tag,
            'pages': posts
        }
        return render(request, 'home/page_list_sport.html', context)

    def reverse_subpage(self, name, args=None, kwargs=None):
        return super().reverse_subpage(name, args, kwargs)

    @route(r"^категория/(?P<cat_slug>[\w-]+)/$", name="category_view")
    def category_view(self, request, cat_slug):
        cat = get_object_or_404(BlogCategory, slug=cat_slug)
        posts = self.get_pages(request=request, cat=cat_slug)
        context = {
            'cat': cat,
            'pages': posts
        }
        return render(request, "home/page_list_sport.html", context)

    def get_absolute_url(self):
        return self.get_url()

    class Meta:
        verbose_name = _(u'Блог')

class BlogPage(Page):
    parent_page_types = ['BlogIndexPage']
    subpage_types = []
    template = 'home/page_sport.html'

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    date_created = models.DateField(verbose_name=_(u'Дата'), 
                                    default=date.today)

    categories = models.ForeignKey('home.BlogCategory', 
                            blank=True,
                            null=True,
                            on_delete=models.SET_NULL,
                            verbose_name=_(u'Категория'))

    content = StreamField([
        ('content', BaseContentBlock(label=_(u'Контент')))
        
    ], verbose_name=_(u'Контент'))

    intro = RichTextField(
        features=['h2', 'h3', 'h4', 'bold', 'italic', \
                'link', 'ol', 'ul'],
        verbose_name=_(u'Предпросмотр'), blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_(u'Изображение')
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('title'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        ImageChooserPanel('image'),
        StreamFieldPanel('content'),
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.Select),
            FieldPanel('date_created'),
        ], heading=_(u"Информация о записи")),
        InlinePanel('comment_sport', label=_(u'Комментарии'))
    ]

    @property
    def get_tags(self):
        tags = self.tags.all()
        for tag in tags:
            tag.url = '/' + '/'.join(s.strip('/') for s in [
                self.get_parent().url,
                'теги',
                tag.slug
            ])
        return tags

    def get_absolute_url(self):
        try:
            site_id, site_root_url, relative_page_path = self.get_url_parts()
            ret = relative_page_path
        except TypeError:
            ret = None
        return ret
    
    class Meta:
        verbose_name_plural = _(u'Записи в блоге')
        verbose_name = _(u'Запись')


class CommentSportPage(XtdComment):
    page = ParentalKey('home.BlogPage', 
                        on_delete=models.CASCADE, 
                        related_name='comment_sport')

    panels = [
        FieldPanel('user'),
        FieldPanel('user_name'),
        FieldPanel('user_email'),
        StreamFieldPanel('comment'),
        FieldPanel('submit_date'),
        FieldPanel('ip_address'),
        FieldPanel('is_public'),
        FieldPanel('is_removed'),
    ]

    def save(self, *args, **kwargs):
        self.page = get_object_or_404(BlogPage, id=self.object_pk)
        return super().save(*args, **kwargs)

class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )
class ContactPage(WagtailCaptchaForm):

    template = "home/contact_page.html"
    subpage_types = []
    parent_page_types = ['HomePage']
    landing_page_template = "home/contact_page.html"

    intro = RichTextField(blank=True, verbose_name=_(u'Сообщение перед формой'))
    thank_you_text = models.TextField(blank=True, verbose_name=_(u'Сообщение при отправление'))

    content_panels = AbstractForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label=_(u'Поля формы')),
        FieldPanel('thank_you_text')
    ]
    class Meta:
        verbose_name = _(u'Страница контактов')
   

@register_setting
class SiteSettings(BaseSetting):
    class Meta:
        verbose_name = _(u'Настройки сайта')

    site_name = models.CharField(
        max_length=255,
        verbose_name=_(u'Название сайта')
    )
    logo_blob = models.TextField(
        verbose_name=_(u'Лого в base64'),
        null=True,
        blank=True,
        editable=True
    )
    site_img = models.ImageField(
        blank=True,
        null=True,
        verbose_name=_(u'Миниатюра')
    )
    site_logo = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='',
        on_delete=models.SET_NULL,
        verbose_name=_(u'Лого')
    )

    count_posts = models.SmallIntegerField(verbose_name=_(u'Количество постов на странице'),
                                            default=9, 
                                            help_text=_(u'Рекомендуется количество постов кратнее 3.'))

    link_vk = models.URLField(verbose_name='VK', blank=True)
    link_inst = models.URLField(verbose_name='Instagram', blank=True)
    link_tele = models.URLField(verbose_name='Telegram', blank=True)

    panels = [
        FieldPanel("site_name"),
        # ImageChooserPanel("site_logo"),
        
        MultiFieldPanel([
            FieldPanel("logo_blob", widget=forms.TextInput(attrs={'size': '40'})),
            FieldPanel("site_img"),
        ], heading=_(u'Лого в базе')),
        
        FieldPanel("count_posts"),
        MultiFieldPanel([
            FieldPanel("link_vk"),
            FieldPanel("link_inst"),
            FieldPanel("link_tele")
        ], heading=_(u'Социальные сети'))
    ]

    def save(self, **kwargs):
        try:
            if self.site_img:
                super(SiteSettings, self).save(**kwargs)
            if os.path.exists(self.site_img.path):
                with open(self.site_img.path,'rb') as file:
                    self.logo_blob = base64.b64encode(file.read()).decode('utf-8')
                    os.remove(self.site_img.path)
                    
            return super(SiteSettings, self).save(**kwargs)
        except BaseException as err:
            print(err)
            pass

class CustomMainMenuItem(AbstractMainMenuItem):
    menu = ParentalKey(
        'wagtailmenus.MainMenu',
        on_delete=models.CASCADE,
        related_name="custom_menu_items", 
    )
    panels = (
        PageChooserPanel('link_page'),
        FieldPanel('link_url'),
        FieldPanel('url_append'),
        FieldPanel('link_text'),
        FieldPanel('link_text_en'),
        FieldPanel('allow_subnav'),
    )