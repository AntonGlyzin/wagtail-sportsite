from django import template
from home.models import CarouselGeneral, BlogCategory
from wagtail.core.models import Page
from taggit.models import Tag
from django.urls import reverse
register = template.Library()


@register.inclusion_tag('includes/carousel_block.html', takes_context=True)
def get_carousel_block(context, gallery):
    images = CarouselGeneral.objects.filter(id=gallery.id)
    if images:
        images = images.first().main_content
    return {
        'images': images,
        'request': context['request']
    }

@register.simple_tag(takes_context=True)
def replace_string(context, string):
    return string.replace('/', '').replace('.', '').replace('_', '')

@register.filter
def div(value, number):
    return int(value) % int(number) == 0

@register.inclusion_tag('includes/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        ancestors = ()
    else:
        ancestors = Page.objects.ancestor_of(
            self, inclusive=True).filter(depth__gt=1)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }

@register.simple_tag(takes_context=True)
def list_category(context):
    cats = BlogCategory.objects.all()
    return cats

@register.simple_tag(takes_context=True)
def list_tags(context):
    tags = Tag.objects.all()
    for item in tags:
        item.url = f'/блог/теги/{item.slug}/'
    return tags