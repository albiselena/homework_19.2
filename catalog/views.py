from catalog.models import Product, Contact
from django.views.generic import ListView, DetailView, TemplateView, CreateView


class CatalogTemplateView(TemplateView):
    template_name = 'catalog/base.html'


class ContactCreateView(CreateView):
    model = Contact
    template_name = 'catalog/contacts.html'
    fields = ['name', 'phone', 'message']
    success_url = '/products/'


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'  # Шаблон, который будет использоваться для отображения списка объектов
    context_object_name = 'products'  # Имя переменной в контексте, в которой будут храниться объекты


class ProductDetailView(DetailView):
    model = Product

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])
