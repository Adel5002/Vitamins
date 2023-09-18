"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from Vitamins.views import PageNotFoundErrorView, ServerErrorView
from .sitemaps import ProductSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'products': ProductSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('Vitamins.urls')),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name="Seo_things/robots.txt", content_type='text/plain')),
    re_path(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
            name='django.contrib.sitemaps.views.sitemap')
]

handler404 = PageNotFoundErrorView.as_view()
handler500 = ServerErrorView.as_view()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
