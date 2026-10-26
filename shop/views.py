from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Product, Tag


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self):
        queryset = Product.objects.filter(
            status='published').order_by('-created_at')
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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if request.user.is_authenticated:
            self.object.viewed_by_users.add(request.user)
        return response


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category', 'manufacturer',
              'tags', 'description', 'price', 'image']
    template_name = 'shop/add_product.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = ['name', 'category', 'manufacturer',
              'tags', 'description', 'price', 'image']
    template_name = 'shop/edit_product.html'

    def test_func(self):
        return self.request.user == self.get_object().owner


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'shop/confirm_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        return self.request.user == self.get_object().owner


# НОВЫЙ КЛАСС: Обработчик добавления/удаления из избранного
class ToggleFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        # Проверяем, есть ли уже этот пользователь в списке добавивших
        if request.user in product.favorited_by.all():
            product.favorited_by.remove(request.user)
            messages.warning(
                request, f'Товар "{product.name}" удален из избранного.')
        else:
            product.favorited_by.add(request.user)
            messages.success(
                request, f'Товар "{product.name}" добавлен в избранное!')

        # Возвращаем пользователя на ту же страницу (каталог или карточку товара)
        return redirect(request.META.get('HTTP_REFERER', 'index'))
