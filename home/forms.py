from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext, gettext_lazy as _, pgettext
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django_comments_xtd.forms import XtdCommentForm
from captcha.fields import ReCaptchaField

class SportCommentForm(XtdCommentForm):
    captcha = ReCaptchaField(label='')
    # email = forms.EmailField(required=False)

class SignupFormSport(SignupForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(
        label=_(u"Имя"),
        widget=forms.TextInput(
            attrs={"placeholder": _(u"Имя")}
        ),
    )
    last_name = forms.CharField(
        label=_("Фамилия"),
        widget=forms.TextInput(
            attrs={"placeholder": _(u"Фамилия")}
        ),
    )
    captcha = ReCaptchaField(label='')
    def save(self, request):
        user = super(SignupFormSport, self).save(request)
        return user

class ProfileSport(ModelForm):
    email = forms.EmailField(disabled=True, required=False, widget=forms.TextInput(
            attrs={"type": "hidden"}
        ))
    username = forms.CharField(disabled=True, label=_(u'Username'))
    first_name = forms.CharField(required=True, label=_(u'Имя'))
    last_name = forms.CharField(required=True, label=_(u'Фамилия'))
    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', ]
        read_only = ['email', 'username',]