from django.contrib.sitemaps import Sitemap
from Vitamins.models import Product

class ProductSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.dateCreation