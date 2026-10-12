from django.contrib import admin
from .models import Category, Manufacturer, Product, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    # Автоматически заполняет slug из названия
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status', 'category', 'created_at')
    list_filter = ('status', 'category', 'manufacturer')
    search_fields = ('name', 'description')

    # Красивый виджет "двойной список" для выбора тегов
    filter_horizontal = ('tags',)
