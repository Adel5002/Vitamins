from django.contrib import admin

from .models import *



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


class CategorytAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategorytAdmin)
admin.site.register(Vendor)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)

