from django.contrib import admin
from django.utils.translation import gettext as _

from home.models import CommentSportPage

from django.templatetags.static import static
from django.utils.html import format_html
from django_comments_xtd.admin import XtdCommentsAdmin
from taggit.models import Tag
from home.models import BlogCategory
from modeltranslation.admin import TranslationAdmin

# admin.site.unregister(Tag)

# @admin.register(Tag)
# class TagAdmin(TranslationAdmin):
#     pass

@admin.register(BlogCategory)
class BlogCategoryAdmin(TranslationAdmin):
    pass

@admin.register(CommentSportPage)
class MyCommentAdmin(XtdCommentsAdmin):
    list_display = ('name', 'submit_date', 'is_public',
                    'is_removed')
    list_display_links = ('name',)
    list_filter = ('is_public', 'is_removed')
    fieldsets = (
        (None,          {'fields': ('content_type', 'object_pk', 'site')}),
        (_('Content'),  {'fields': ('user', 'user_name', 'user_email',
                                  'user_url', 'comment', 'followup')}),
        (_('Metadata'), {'fields': ('submit_date', 'ip_address',
                                    'is_public', 'is_removed')}),
    )