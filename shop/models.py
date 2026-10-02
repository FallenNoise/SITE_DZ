from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена")

    image = models.ImageField(
        upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Продавец", null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
