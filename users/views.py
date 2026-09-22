from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем пользователя и сразу авторизуем его
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()

    return render(request, 'users/register.html', {'form': form})

# Декоратор защищает страницу: если гость попытается зайти, его кинет на login


@login_required
def profile(request):
    return render(request, 'users/profile.html')
