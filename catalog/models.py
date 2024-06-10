from django.db import models

NULLABLE = {"null": True, "blank": True}


class Product(models.Model):
    name = models.CharField(
        max_length=100, verbose_name="Название", help_text="Введите название товара"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание товара"
    )
    image = models.ImageField(upload_to="products/", verbose_name="Фото", **NULLABLE)
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Категория",
        related_name="products",
    )
    price = models.IntegerField(verbose_name="Цена", help_text="Введите цену товара")
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name="Дата изменения",
        auto_now=True,
    )


    def __str__(self):
        return f"{self.name} ({self.category}) - {self.price} руб."

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Наименование",
        help_text="Введите название категории",
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание категории", **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]
