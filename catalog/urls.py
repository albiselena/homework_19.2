from django.urls import path

from catalog.views import CatalogTemplateView, ProductDetailView, ProductListView, ContactCreateView, BlogListView, \
    BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'catalog'

urlpatterns = [
    path('', CatalogTemplateView.as_view(), name='index'),
    path('products/', ProductListView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('contacts/', ContactCreateView.as_view(), name='contacts'),
    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog/<int:pk>/update/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='blog_delete')

]
