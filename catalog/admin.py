from django.contrib import admin
from catalog.models import Category, Product, Version


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
#    list_filter = ('name', 'description',)
#    search_fields = ('name', 'description',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'category', 'is_published',)
    list_filter = ('category', 'is_published', )
    search_fields = ('name', 'description',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('product', 'number_version', 'title_version', 'is_active',)
    list_filter = ('number_version',)
    search_fields = ('number_version', 'title_version',)
