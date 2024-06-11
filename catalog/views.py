from django.shortcuts import render
from catalog.models import Product, Contact


def home(request):
    # Сортируем по дате создания и берем первые 3 товара с помощью -created_at
    latest_products = Product.objects.order_by('-created_at')[:3]

    # Выводим названия товаров в консоль
    for product in latest_products:
        print(product.name)

    return render(request, 'home.html')


def contacts(request):
    contact = Contact.objects.all()  # Получаем все объекты из модели Contact
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'{name} ({phone}): {message}')

    return render(request, 'contacts.html', {'contacts': contact})
