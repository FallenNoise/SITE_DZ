from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from shop.models import Product, Order  # Импортируем модели из приложения shop


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # Собираем все необходимые коллекции для личного кабинета
    my_products = Product.objects.filter(
        owner=request.user).order_by('-created_at')
    favorites = request.user.favorite_products.all()
    history = request.user.viewed_products.all()
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'users/profile.html', {
        'my_products': my_products,
        'favorites': favorites,
        'history': history,
        'orders': orders
    })
