from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):
    help = "Эта команда заполняет базу данных из файла json."

    def handle(self, *args, **options):
        # Очищаем таблицы
        Category.objects.all().delete()
        Product.objects.all().delete()

        with open('catalog/fixtures/catalog_data.json', 'r', encoding='utf8') as file:
            # Загружаем данные из файла
            data = json.load(file)

        category_list = []
        product_list = []

        for item in data:
            model = item['model']

            if model == 'catalog.category':
                category_list.append(Category(
                    id=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields']['description'],
                ))

        Category.objects.bulk_create(category_list)

        for item in data:
            model = item['model']

            if model == 'catalog.product':
                product_list.append(Product(
                    id=item['pk'],
                    name=item['fields']['name'],
                    description=item['fields']['description'],
                    image=item['fields']['image'],
                    category_id=item['fields']['category'],
                    price=item['fields']['price'],
                ))

        Product.objects.bulk_create(product_list)