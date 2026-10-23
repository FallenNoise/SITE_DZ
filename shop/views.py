from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, Tag

# 1. Каталог с фильтрацией и ПАГИНАЦИЕЙ


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 6  # Django сам разобьет товары по 6 штук на страницу

    def get_queryset(self):
        # Базовая выборка: только опубликованные, сортировка от новых к старым
        queryset = Product.objects.filter(
            status='published').order_by('-created_at')

        # Проверяем, есть ли фильтрация по тегу
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            self.tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=self.tag)
        else:
            self.tag = None

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_tag'] = self.tag
        context['all_tags'] = Tag.objects.all()
        return context

# 2. Карточка товара с ФИКСАЦИЕЙ ПРОСМОТРОВ


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        # Сначала получаем объект товара
        response = super().get(request, *args, **kwargs)
        # Если юзер авторизован, добавляем его в историю просмотров этого товара
        if request.user.is_authenticated:
            # add() работает умно: если юзер уже есть в списке, он не продублируется
            self.object.viewed_by_users.add(request.user)
        return response

# 3. Создание товара


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'manufacturer',
              'tags', 'description', 'price', 'image']
    template_name = 'shop/add_product.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# 4. Редактирование товара (только для владельца)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'manufacturer',
              'tags', 'description', 'price', 'image']
    template_name = 'shop/edit_product.html'

    def test_func(self):
        return self.request.user == self.get_object().owner

# 5. Удаление товара (только для владельца)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'shop/confirm_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user == self.get_object().owner
