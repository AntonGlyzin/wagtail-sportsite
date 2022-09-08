from .base import *
from dotenv import load_dotenv

DEBUG = True


path_env = os.path.join(BASE_DIR, '.env')
load_dotenv(path_env)


SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ["*"]

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "mysport.db"),
    }
}


try:
    from .local import *
except ImportError:
    pass
