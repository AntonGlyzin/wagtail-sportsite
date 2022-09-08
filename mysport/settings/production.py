from .base import *
import dj_database_url
import os

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    "default": dj_database_url.config()
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ["*"]


try:
    from .local import *
except ImportError:
    pass
