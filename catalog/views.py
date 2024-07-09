from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.utils.text import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Contact, Blog, Version
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView


class ProductFormsetMixin:
    """Миксин для формсета продуктов"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ProductFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.POST:
            context['formset'] = ProductFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = ProductFormset(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class ProductVersionMixin:
    """Миксин для добавления активной версии продукта в контекст."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if isinstance(self, ListView):
            products = context.get('object_list', [])
            for product in products:
                version = Version.objects.filter(product=product, is_active=True).last()
                product.active_version = version.version_name if version else 'Нет активной версии'
        elif isinstance(self, DetailView):
            product = context.get('product')
            if product:
                version = Version.objects.filter(product=product, is_active=True).last()
                product.active_version = version.version_name if version else 'Нет активной версии'
        return context


class ProductListView(ProductVersionMixin, ListView):
    """Список продуктов."""
    model = Product


class ProductDetailView(ProductVersionMixin, DetailView):
    """Подробная информация о продукте."""
    model = Product


class ProductCreateView(ProductFormsetMixin, CreateView):
    """Добавление нового продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')


class ProductUpdateView(ProductFormsetMixin, UpdateView):
    """Редактирование продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')


class ProductDeleteView(DeleteView):
    """Удаление продукта."""
    model = Product
    success_url = reverse_lazy('catalog:products')


class CatalogTemplateView(TemplateView):
    """Шаблон каталога."""
    template_name = 'catalog/base.html'


class ContactCreateView(CreateView):
    """Добавление нового контакта."""
    model = Contact
    template_name = 'catalog/contacts.html'
    fields = ['name', 'phone', 'message']
    success_url = '/products/'


class BlogListView(ListView):
    """Список блогов."""
    model = Blog
    fields = ('title', 'text', 'preview', 'created_at', 'publication')
    success_url = reverse_lazy('blog:blog')

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class BlogDetailView(DetailView):
    """Подробная информация о блоге."""
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    """Добавление нового блога."""
    model = Blog
    fields = ['title', 'text', 'preview', 'publication']
    success_url = reverse_lazy('catalog:blog')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    """Редактирование блога."""
    model = Blog
    fields = ['title', 'text', 'preview', 'publication']

    def get_success_url(self):
        return reverse_lazy('catalog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление блога."""
    model = Blog
    success_url = reverse_lazy('catalog:blog')
