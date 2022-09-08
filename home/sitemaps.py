from django.contrib.sitemaps import Sitemap
from home.models import BlogPage, BlogIndexPage, PageProgram, IndexProgram
from django.urls import reverse

class  ProgramPostitemap(Sitemap):
    priority = 0.9
    protocol = 'https'
    def items(self):
        return PageProgram.objects.live().order_by('-first_published_at')
    def lastmod(self, obj):
        return obj.date_created

class  BlogPostitemap(Sitemap):
    priority = 0.9
    protocol = 'https'
    def items(self):
        return BlogPage.objects.live().order_by('-first_published_at')
    def lastmod(self, obj):
        return obj.date_created

class  StaticBlogMap(Sitemap):
    priority = 0.9
    protocol = 'https'
    def items(self):
        return BlogIndexPage.objects.live().order_by('-first_published_at')

class  StaticProgramMap(Sitemap):
    priority = 0.9
    protocol = 'https'
    def items(self):
        return IndexProgram.objects.live().order_by('-first_published_at')