from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import slugify

from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Contact, Blog, Version, Category
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from catalog.services import get_categories_from_cache


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


class CategoryListView(ListView):
    """Список категорий."""
    model = Category

    def get_queryset(self):
        return get_categories_from_cache()


class ProductListView(ProductVersionMixin, ListView):
    """Список продуктов."""
    model = Product


class ProductDetailView(DetailView):
    """Подробная информация о продукте."""
    model = Product


class ProductCreateView(LoginRequiredMixin, ProductFormsetMixin, CreateView):
    """Добавление нового продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')
    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        # Метод для связывания продукта с пользователем
        product = form.save(commit=False)
        product.owner = self.request.user  # Присваиваем владельца продукта
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)


class ProductUpdateView(LoginRequiredMixin, ProductFormsetMixin, UpdateView):
    """Редактирование продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:products')
    login_url = 'users:login'
    redirect_field_name = "redirect_to"

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return ProductForm
        if (user.has_perm('catalog.can_edit_publication')
                and user.has_perm('catalog.can_edit_description')
                and user.has_perm('catalog.can_edit_category')):
            return ProductModeratorForm
        raise PermissionDenied("У вас нет прав для редактирования этого продукта.")


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта."""
    model = Product
    success_url = reverse_lazy('catalog:products')

    login_url = 'users:login'
    redirect_field_name = "redirect_to"


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
