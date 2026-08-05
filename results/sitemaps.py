from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import NewsUpdate, Constituency


class StaticViewSitemap(Sitemap):
    protocol = "https"
    priority = 0.9
    changefreq = "daily"

    def items(self):
        return [
            "home",
            "about",
            "contact",
            "news_list",
            "constituencies",
            "privacy_policy",
            "terms_and_conditions",
        ]

    def location(self, item):
        return reverse(item)


class NewsSitemap(Sitemap):
    protocol = "https"
    priority = 0.8
    changefreq = "hourly"

    def items(self):
        return NewsUpdate.objects.all()

    def lastmod(self, obj):
        return obj.created_at

    def location(self, obj):
        return reverse(
            "news_detail",
            args=[obj.id]
        )


class ConstituencySitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "daily"

    def items(self):
        return Constituency.objects.all()

    def location(self, obj):
        return reverse(
            "constituency_detail",
            args=[obj.id]
        )