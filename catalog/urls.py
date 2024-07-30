from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.views import CatalogTemplateView, ProductDetailView, ProductListView, ContactCreateView, BlogListView, \
    BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, CategoryListView

app_name = 'catalog'

urlpatterns = [
    path('', CatalogTemplateView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    path('contacts/', ContactCreateView.as_view(), name='contacts'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete'),
    path('create/product/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('category', CategoryListView.as_view(), name='category'),

]
