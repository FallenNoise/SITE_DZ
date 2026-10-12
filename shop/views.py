from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Tag


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Показываем только товары со статусом "Опубликовано", сортируем по новизне
        queryset = Product.objects.filter(
            status='published').order_by('-created_at')

        # Если в URL передан тег, дополнительно фильтруем по нему
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
        # Передаем все теги для кнопок-фильтров
        context['all_tags'] = Tag.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
