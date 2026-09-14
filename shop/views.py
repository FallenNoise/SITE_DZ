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

            return redirect('index')
    else:
        form = ProductForm()

    return render(request, 'shop/add_product.html', {'form': form})


def edit_product(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()

            return redirect('index')
    else:

        form = ProductForm(instance=product)

    return render(request, 'shop/edit_product.html', {'form': form, 'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()

        return redirect('index')

    return render(request, 'shop/confirm_delete.html', {'product': product})
