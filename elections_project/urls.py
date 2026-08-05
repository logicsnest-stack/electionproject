from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from results.sitemaps import (
    StaticViewSitemap,
    NewsSitemap,
    ConstituencySitemap,
)

sitemaps = {
    "static": StaticViewSitemap,
    "news": NewsSitemap,
    "constituencies": ConstituencySitemap,
}

urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("results.urls")),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )