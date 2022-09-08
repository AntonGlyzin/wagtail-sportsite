"""
Django settings for mysport project.

Generated by 'django-admin startproject' using Django 4.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

INSTALLED_APPS = [
    "home",
    "search",
    'sass_processor',
    'django_extensions',
    "wagtailseo",
    
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    'captcha',
    'wagtailcaptcha',
    "taggit",
    'wagtailfontawesome',
    
    'wagtail.contrib.modeladmin',
    'wagtail.contrib.styleguide',
    "wagtail.contrib.routable_page",
    'wagtailmenus',

    'modeltranslation',
    'wagtail.contrib.settings',
    "django.contrib.admin",
    'django.contrib.sites',
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    'django.contrib.sitemaps',

    'django_comments_xtd',
    'django_comments',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'authuser',
    'coverage',
    'robots'
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware"
]

ROOT_URLCONF = "mysport.urls"
SITE_ID = 333

AUTH_USER_MODEL = 'authuser.User'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'wagtail.contrib.settings.context_processors.settings'
            ],
        },
    },
]

WSGI_APPLICATION = "mysport.wsgi.application"


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'sass_processor.finders.CssFinder', 
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]


STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

LOCALE_PATHS = (
	os.path.join(BASE_DIR, 'locale'),
)

WAGTAIL_SITE_NAME = "mysport"

WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}
# WAGTAILSTREAMFORMS_ADVANCED_SETTINGS_MODEL = None
# WAGTAILSTREAMFORMS_ADMIN_MENU_ORDER = None
# WAGTAILSTREAMFORMS_ADMIN_MENU_LABEL = 'Streamforms'

WAGTAILMENUS_MAIN_MENU_ITEMS_RELATED_NAME = "custom_menu_items"

WAGTAILADMIN_BASE_URL = "http://example.com"

WAGTAIL_I18N_ENABLED = True

WAGTAIL_USER_EDIT_FORM = 'authuser.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'authuser.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['photo', ]

WAGTAIL_CONTENT_LANGUAGES = LANGUAGES  = (
	('ru', u'Русский'), 
	('en', 'English'),
)
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

RECAPTCHA_PUBLIC_KEY = "6Lehep4hAAAAAJG894VMVCc5HfmBKYS6YSockfCN"
RECAPTCHA_PRIVATE_KEY = "6Lehep4hAAAAADF8IHqK6qwyZVAssDF-VP20XDhZ"
NOCAPTCHA = True

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMMENTS_APP = 'django_comments_xtd'
COMMENTS_XTD_MAX_THREAD_LEVEL = 2
COMMENTS_XTD_CONFIRM_EMAIL = False
COMMENTS_XTD_MARKUP_FALLBACK_FILTER = 'markdown'
COMMENTS_XTD_APP_MODEL_OPTIONS = {
    'home.blogpage': {
        'allow_flagging': True,
        'allow_feedback': True,
        'show_feedback': True,
    }
}
COMMENTS_XTD_MODEL = 'home.models.CommentSportPage'
COMMENTS_XTD_FORM_CLASS = 'home.forms.SportCommentForm'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_FORMS = {'signup': 'home.forms.SignupFormSport'}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = "smtp.mail.ru"
# EMAIL_PORT = 2525
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# DEFAULT_FROM_EMAIL = ""
# SERVER_EMAIL = ''

WAGTAILEMBEDS_RESPONSIVE_HTML = True