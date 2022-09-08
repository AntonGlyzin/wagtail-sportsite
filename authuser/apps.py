from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AuthuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authuser'
    verbose_name = _('Users')
