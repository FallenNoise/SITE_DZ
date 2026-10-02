from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Какие столбцы показывать в списке товаров
    list_display = ('name', 'price', 'owner', 'status', 'created_at')

    # По каким полям можно фильтровать товары сбоку
    list_filter = ('status', 'created_at')

    # Делает поле статуса редактируемым прямо в общем списке!
    list_editable = ('status',)
