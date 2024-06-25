from django.urls import reverse_lazy
from django.utils.text import slugify
from catalog.models import Product, Contact, Blog
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView


class CatalogTemplateView(TemplateView):
    template_name = 'catalog/base.html'


class ContactCreateView(CreateView):
    model = Contact
    template_name = 'catalog/contacts.html'
    fields = ['name', 'phone', 'message']
    success_url = '/products/'


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])


class BlogListView(ListView):
    model = Blog
    fields = ('title', 'text', 'preview', 'created_at', 'publication')
    success_url = reverse_lazy('blog:blog')

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(publication=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
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
    model = Blog
    fields = ['title', 'text', 'preview', 'publication']

    def get_success_url(self):
        return reverse_lazy('catalog:blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog')
