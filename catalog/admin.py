from django.contrib import admin

from catalog.models import Category, Product, Contact


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Администрирование товаров
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category', 'name', 'price',)
    search_fields = ('name', 'description', 'category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Администрирование категорий
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name', 'description',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Администрирование контактов
    list_display = ('name', 'phone', 'message',)
