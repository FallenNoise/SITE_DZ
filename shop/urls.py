from django.urls import path
from .views import ProductListView, ProductDetailView

urlpatterns = [
    # Главная страница (каталог)
    path('', ProductListView.as_view(), name='index'),

    # Каталог, отфильтрованный по тегу
    path('tag/<slug:tag_slug>/', ProductListView.as_view(),
         name='product_list_by_tag'),

    # Карточка товара (у вас используется id, поэтому <int:pk>)
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
