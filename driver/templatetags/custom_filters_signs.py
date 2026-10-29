

from django import template
import re
from django.utils.safestring import mark_safe
from urllib.parse import quote

register = template.Library()


@register.filter
def linkify_signs(value, args):
    """Автоматически превращает номера знаков в ссылки с картинками."""

    # Обработка аргументов
    if isinstance(args, str):
        try:
            args = dict(arg.split('=') for arg in args.split(','))
        except ValueError:
            args = {'topic_id': 'default_topic', 'category_id': 'default_category'}

    topic_id = args.get('topic_id', 'default_topic')
    category_id = args.get('category_id', 'default_category')

    # Удаляем старые ссылки и изображения
    value = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', value)
    value = re.sub(r'<img[^>]*>', '', value)

    # Ищем только номера знаков (например, 7.1 или 7.1.1)
    pattern = r'\b\d{1,2}\.\d{1,2}(?:\.\d{1,2})?\b'

    def replace_match(match):
        sign_number = match.group(0)

        encoded_sign_number = quote(sign_number, safe="")

        link = f'<a href="/topic/{topic_id}/categories/{category_id}/signs/{sign_number}/">{sign_number}</a>'

        # Кодируем только путь к изображению
        image = f'<img src="/media/sign/{encoded_sign_number}.webp" class="sign-image">'
        return f'{link} {image}'

    return mark_safe(re.sub(pattern, replace_match, value))


