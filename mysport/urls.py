from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from home.views import Profile
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps import views
from home.sitemaps import (BlogPostitemap, ProgramPostitemap, 
StaticBlogMap, StaticProgramMap)

sitemaps = {
    'blog': BlogPostitemap,
    'program': ProgramPostitemap,
    'index-program': StaticProgramMap,
    'index-blog': StaticBlogMap,
}

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
    path('i18n/', include('django.conf.urls.i18n')),
    re_path(r'^robots\.txt', include('robots.urls')),
    path('sitemap.xml', views.index, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('comments/', include('django_comments_xtd.urls')),
    path('accounts/profile/', Profile.as_view(), name='user_profile'),
    path('accounts/', include('allauth.urls')),
    path("", include(wagtail_urls)),
)

# urlpatterns = urlpatterns + [
#     path("", include(wagtail_urls)),
# ]
