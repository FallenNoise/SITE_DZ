from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена")

    # image = models.ImageField(upload_to='products/', blank=True)

    # ИСПРАВЛЕНИЕ: Добавлен отступ в 4 пробела перед created_at
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # 'product_detail' — это имя маршрута из urls.py (см. Шаг 3)
        return reverse('product_detail', args=[str(self.id)])
