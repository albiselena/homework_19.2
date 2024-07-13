from django.contrib import admin

from catalog.models import Category, Product, Contact, Blog, Version
from users.models import User


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


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    # Администрирование версий
    list_display = ('product', 'version_number', 'version_name', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('version_number',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Администрирование контактов
    list_display = ('name', 'phone', 'message',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Администрирование блога
    list_display = ('title', 'created_at', 'publication',)
    list_filter = ('title', 'publication', 'created_at',)
    search_fields = ('title', 'text', 'created_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Администрирование пользователей
    list_display = ('email', 'phone', 'country', 'avatar',)
    list_filter = ('email', 'country',)
    search_fields = ('email', 'phone', 'country',)