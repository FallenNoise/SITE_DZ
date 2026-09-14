from django.shortcuts import render, redirect, get_object_or_404
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


def edit_product(request, product_id):
    # Получаем товар по ID или выдаем 404 ошибку
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Передаем данные из запроса и указываем instance=product,
        # чтобы Django понял, что мы обновляем существующую запись, а не создаем новую
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            # Укажите здесь имя вашего маршрута списка товаров (например, 'catalog' или 'product_list')
            return redirect('product_list')
    else:
        # Если метод GET, просто заполняем форму текущими данными товара
        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Удаление должно происходить только через POST-запрос для безопасности
    if request.method == 'POST':
        product.delete()
        # Замените 'catalog' на имя вашего маршрута списка товаров
        return redirect('catalog')

    # Если метод GET, показываем страницу подтверждения удаления
    return render(request, 'shop/confirm_delete.html', {'product': product})
