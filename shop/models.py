from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Владелец"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
