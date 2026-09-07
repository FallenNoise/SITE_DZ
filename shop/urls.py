from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='index'),
    path('add/', views.add_product, name='add_product'),
]
