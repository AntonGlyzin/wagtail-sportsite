from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from authuser.models import User
from django.utils.translation import gettext_lazy as _
# from authuser.forms import CustomUserEditForm, CustomUserCreationForm
from django.utils.safestring import mark_safe
from django.shortcuts import render

class CustomUserEditForm(UserChangeForm):
    photo = forms.ImageField(required=False, label=_(u"Изображение"))


class CustomUserCreationForm(UserCreationForm):
    photo = forms.ImageField(required=False, label=_(u"Изображение"))

@admin.register(User)
class SportUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserEditForm
    model = User
    list_display = ['username',  'get_html_photo', 'is_active', 'is_superuser', 'is_staff']
    readonly_fields = ['get_html_photo']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'photo')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (_(u'Аватарка'), {'fields': ('photo', 'get_html_photo')}),
    )
    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f'<img src={object.photo.url} width=112>')
    get_html_photo.short_description = _(u"Миниатюра")
