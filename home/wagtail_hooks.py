from wagtail.contrib.modeladmin.options import (
                        ModelAdmin, 
                        ModelAdminGroup, 
                        modeladmin_register)

from home.models import (CarouselGeneral, 
                        TestimonialSport, 
                        BlogCategory, 
                        CommentSportPage,
                        SiteSettings)
from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks
from django.utils.translation import gettext_lazy as _
from taggit.models import Tag
from django.utils.safestring import mark_safe
from authuser.models import User
from wagtail.images.views.bulk_actions.image_bulk_action import ImageBulkAction
from wagtail.admin.views.bulk_action import BulkAction
from wagtail import hooks
from wagtail.admin.views.bulk_action import BulkAction
from wagtail.admin.views.pages.bulk_actions.page_bulk_action import PageBulkAction



@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/mysport.css')
    )

class CarouselGeneralAdmin(ModelAdmin):
    model = CarouselGeneral
    list_display = ('text', )
    search_fields = ('text',)
    menu_label = _(u'Карусель') 
    menu_icon = 'fa-picture-o' 

class TestimonialSportAdmin(ModelAdmin):
    model = TestimonialSport
    list_display = ('author', 'get_html_photo' )
    search_fields = ('author',)
    menu_label = _(u'Рекомендации') 
    menu_icon = 'fa-comment'
    date_hierarchy = 'submit_date'

    def get_html_photo(self, object):
        if object.image:
            url = object.image.get_rendition('fill-90x90').url
            return mark_safe(f"<img src='{url}' style='border-radius:50%;' width=90>")
        return mark_safe(f"<img src='' width=90>")
    get_html_photo.short_description = _(u"Миниатюра")

class CategorySportAdmin(ModelAdmin):
    model = BlogCategory
    list_display = ('name', )
    search_fields = ('name',)
    menu_label = _(u'Категории') 
    menu_icon = 'fa-bookmark' 

class CommentSportPageAdmin(ModelAdmin):
    model = CommentSportPage
    list_display = ('name', 'get_html_photo' ,'comment', 'submit_date', 'is_public',  'is_removed')
    list_filter = ['is_public',  'is_removed']
    search_fields = ('name',)
    menu_label = _(u'Комментарии') 
    menu_icon = 'fa-comments' 

    def get_html_photo(self, object):
        if object.user and object.user.photo:
            url = object.user.photo.url
            return mark_safe(f"<img src='{url}' style='border-radius:50%;' width=90>")
        return mark_safe(f"<img src='' width=90>")
    get_html_photo.short_description = _(u"Миниатюра")


class TagAdmin(ModelAdmin):
    model = Tag
    list_display = ('name', )
    search_fields = ('name',)
    menu_label = _(u'Теги')
    menu_icon = 'fa-tags' 
    prepopulated_fields = {"slug": ("name",)}
    
@modeladmin_register
class StaticModelAdminGroup(ModelAdminGroup):
    menu_label = _(u'Элементы сайта')
    menu_icon = 'fa-cubes'  
    menu_order = 300  
    items = (CarouselGeneralAdmin, 
            TestimonialSportAdmin,
            CategorySportAdmin,
            CommentSportPageAdmin,
            TagAdmin)

