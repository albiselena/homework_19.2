from datetime import datetime
from django import template

register = template.Library()


@register.filter
def slice_by_space(text, length):
    """Фильтр для обрезки текста по пробелу"""
    if len(text) <= length:
        return text
    else:
        return ' '.join(text[:length + 1].split(' ')[0:-1]) + '...'


@register.filter
def media_filter(value):
    """Фильтр для вывода пути к медиафайлу"""
    if value:
        return f'/media/{value}'
    return 'нет картинки'
