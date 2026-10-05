from django.contrib import admin
from .models import Product, Category, Manufacturer

# Регистрируем Категории


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Регистрируем Производителей


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'website')

# Обновляем Товары (ваши настройки сохранены, добавлены новые поля)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'manufacturer',
                    'owner', 'status', 'created_at')
    list_filter = ('status', 'category', 'manufacturer', 'created_at')
    list_editable = ('status',)
