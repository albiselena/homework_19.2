from django import template

register = template.Library()


@register.filter
def slice_by_space(text, length):
    """Фильтр для обрезки текста по пробелу"""
    if len(text) <= length:
        return text
    else:
        return ' '.join(text[:length + 1].split(' ')[0:-1]) + '...'
