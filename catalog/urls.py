from django.urls import path

from catalog.views import index, product_details, products, contacts

app_name = 'catalog'

urlpatterns = [
    path('', index),
    path('products/', products, name='products'),
    path('products/<int:pk>/', product_details, name='product_details'),
    path('contacts/', contacts, name='contacts')
]
