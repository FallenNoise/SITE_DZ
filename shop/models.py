from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name="Имя тега")
    slug = models.SlugField(max_length=50, unique=True,
                            verbose_name="URL-метка")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_tag', args=[self.slug])


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(
        verbose_name="Описание", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Manufacturer(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    website = models.URLField(verbose_name="Сайт", blank=True, null=True)
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Product(models.Model):
    STATUS_CHOICES = [
        ('pending', 'На проверке'),
        ('published', 'Опубликовано'),
        ('rejected', 'Отклонено'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Производитель")
    tags = models.ManyToManyField(
        Tag, related_name='products', blank=True, verbose_name="Теги")

    # НОВОЕ ПОЛЕ: Связь с пользователями для учета просмотров
    viewed_by_users = models.ManyToManyField(
        User, related_name='viewed_products', blank=True, verbose_name="Просмотрели пользователи")

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
