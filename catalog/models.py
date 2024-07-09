from django.db import models, connection

NULLABLE = {"null": True, "blank": True}


class Product(models.Model):
    # Таблица товаров
    name = models.CharField(
        max_length=100, verbose_name="Название", help_text="Введите название товара"
    )
    description = models.TextField(
        verbose_name="Описание", help_text="Введите описание товара", **NULLABLE
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
    # Таблица категорий
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


class Version(models.Model):
    # Таблица версий
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="versions", verbose_name="Продукт")
    version_number = models.IntegerField(verbose_name="Номер версии")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    is_active = models.BooleanField(default=True, verbose_name="Активная версия")

    def __str__(self):
        return f"{self.product} - {self.version_name} ({self.version_number})"

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["-version_number"]


class Contact(models.Model):
    # Таблица контактов и сообщений
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["-created_at"]


class Blog(models.Model):
    # Таблица для блога
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    slug = models.CharField(max_length=50, verbose_name="Слаг", **NULLABLE)
    text = models.TextField(verbose_name="Текст")
    preview = models.ImageField(upload_to="blog/", verbose_name="Превью", **NULLABLE)
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    publication = models.BooleanField(default=True, verbose_name="Опубликовано")
    number_of_views = models.IntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f'{self.title} - {self.created_at}'

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-created_at"]
