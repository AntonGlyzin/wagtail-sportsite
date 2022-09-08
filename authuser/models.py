from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

def user_directory_path(instance, filename):
    return 'avatars/{0}/{1}'.format(instance.username, filename)

class User(AbstractUser):
    photo = models.ImageField(
        blank=True,
        null=True,
        verbose_name=_(u'Фото'),
        upload_to = user_directory_path
    )

    class Meta:
        verbose_name_plural = _(u'Профиль')
        verbose_name = _(u'Профиль')