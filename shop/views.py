from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'shop/index.html', {'products': products})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Убедитесь, что 'index' - это имя маршрута главной страницы каталога
            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})
