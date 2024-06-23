from django.db import models

NULLABLE = {'null': True, 'blank': True}

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    slug = models.CharField(max_length=100, verbose_name='Слаг', **NULLABLE)
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog', verbose_name='Превью', **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    publication_sing = models.BooleanField(default=False, verbose_name='Опубликовано')
    number_of_views = models.IntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return f'{self.title}, {self.created_at}, {self.publication_sing}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'


