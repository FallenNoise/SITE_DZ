from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def product_detail(request, id):
    # Ищем товар по ID. Если не найден — отдаем 404
    product = get_object_or_404(Product, id=id)

    # Передаем объект товара в шаблон
    return render(request, 'shop/product_detail.html', {'product': product})


def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'shop/index.html', {'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Создаем объект товара, но приостанавливаем сохранение в БД
            product = form.save(commit=False)

            # Присваиваем текущего авторизованного пользователя
            product.owner = request.user

            # Теперь окончательно сохраняем товар в базу данных
            product.save()

            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})


@login_required
def edit_product(request, product_id):
    # Ищем товар в базе данных
    product = get_object_or_404(Product, id=product_id)

    # ПРОВЕРКА ПРАВ: Если владелец товара не совпадает с текущим пользователем
    # null (None) проверка нужна на случай, если у старых товаров вообще нет владельца
    if product.owner != request.user:
        raise PermissionDenied("Вы не можете редактировать чужой товар.")
        # Альтернативно, вместо ошибки можно просто вернуть на главную:
        # return redirect('index')

    if request.method == 'POST':
        # Передаем instance=product, чтобы форма знала, какой товар обновлять
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # Здесь commit=False не нужен, так как владелец уже привязан к товару
            form.save()
            # Укажите здесь имя вашего URL для возврата
            return redirect('index')
    else:
        form = ProductForm(instance=product)

    # Используем тот же шаблон, что и для добавления (или 'shop/edit_product.html', если он у вас отдельный)
    return render(request, 'shop/add_product.html', {'form': form})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()

        return redirect('index')

    return render(request, 'shop/confirm_delete.html', {'product': product})
