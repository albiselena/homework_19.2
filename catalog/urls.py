from django.urls import path

from catalog.views import CatalogTemplateView, ProductDetailView, ProductListView, ContactCreateView

app_name = 'catalog'

urlpatterns = [
    path('', CatalogTemplateView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactCreateView.as_view(), name='contacts')
]
