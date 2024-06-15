from django.shortcuts import render, get_object_or_404
from catalog.models import Product, Contact


def index(request):
    return render(request, 'base.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contact.objects.create(name=name, phone=phone, message=message)
        return render(request, 'contacts.html', {'message': 'Ваше сообщение отправлено!'})
    return render(request, 'contacts.html')


def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_details.html', context)
