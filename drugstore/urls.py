from django.urls import path
from . import views

app_name = 'drugstore'

urlpatterns = [
    path('', views.get_product_list, name='product_list'),
    path('search_product/', views.search_product, name='search'),
    path('add-product/', views.create_product, name='add_product'),
    path('update-product/<str:product_slug>/', views.update_product, name='update_product'),
    path('delete/<str:product_slug>/', views.delete_product, name='delete_product'),
    path('product-like/<int:id>/', views.like_product, name="product_like_url"),
    path('product/detail/<str:product_slug>/', views.get_product_detail, name='product_details'),
    path('products/<str:product_slug>/', views.get_product_detail, name='product_details'),
    path('export/', views.write_db),
    path('<str:category_slug>/', views.get_product_list, name='product_list_by_category'),
]
