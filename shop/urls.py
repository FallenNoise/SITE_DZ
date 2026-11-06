from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ToggleFavoriteView,
    AddCommentView
)

urlpatterns = [
    # Главная страница и фильтрация по тегам
    path('', ProductListView.as_view(), name='index'),
    path('tag/<slug:tag_slug>/', ProductListView.as_view(),
         name='product_list_by_tag'),

    # CRUD операции для товаров
    path('product/add/', ProductCreateView.as_view(), name='add_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/delete/',
         ProductDeleteView.as_view(), name='delete_product'),

    # Избранное
    path('product/<int:pk>/favorite/',
         ToggleFavoriteView.as_view(), name='toggle_favorite'),

    # Добавление комментария
    path('product/<int:pk>/comment/',
         AddCommentView.as_view(), name='add_comment'),
]
