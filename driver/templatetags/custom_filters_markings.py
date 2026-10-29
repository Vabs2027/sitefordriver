import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def linkify_markings(value, args):
    """Автоматически превращает номера разметки и знаков в ссылки с картинками."""

    if isinstance(args, str):
        try:
            args = dict(arg.split('=') for arg in args.split(','))
        except ValueError:
            args = {'topic_id': '34', 'category_id': 'default_category'}

    topic_id = args.get('topic_id', '34')
    category_id = args.get('category_id', 'default_category')

    # Удаляем старые ссылки и картинки
    value = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', value)
    value = re.sub(r'<img[^>]*>', '', value)

    # Регулярные выражения
    marking_pattern = r'\b(?:розмітка|суцільній|розмітці|розмітку|розміткою|лінія|лінію)\s*(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\b'
    sign_with_text_pattern = r'\b(знаками|знаком|знак|знака)\s+((?:\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)(?:\s*,\s*\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)*)\b'
    standalone_number_pattern = r'\b(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\b'

    used_links = set()  # Запоминаем уже замененные номера

    def replace_marking(match):
        """Создаёт ссылку для разметки."""
        marking_number = match.group(1).strip()

        if marking_number in used_links:
            return marking_number  # Если уже заменяли – просто вернуть текст

        used_links.add(marking_number)

        image_file_name = f"rozkitka_{marking_number}.webp"
        image_path = f"/media/markings/{image_file_name}"
        link = f'<a href="/topic/{topic_id}/categories/1/markings/{marking_number}/">{marking_number}</a>'
        image = f'<img src="{image_path}" class="markings-image">'

        return f'{link} {image}'

    def replace_sign_numbers(match):
        """Заменяет КАЖДЫЙ номер знака в списке."""
        text_part = match.group(1)  # Например, "знаками"
        sign_numbers = match.group(2)  # Например, "5.46.1, 5.46.2"

        links = []
        for sign_number in sign_numbers.split(','):
            sign_number = sign_number.strip()
            if sign_number in used_links:
                links.append(sign_number)  # Если уже заменяли, просто вернуть текст
            else:
                used_links.add(sign_number)
                sign_link = f'<a href="/topic/33/categories/1/signs/{sign_number}/">{sign_number}</a>'
                sign_image = f'<img src="/media/sign/{sign_number}.webp" class="sign-image">'
                links.append(f'{sign_link} {sign_image}')

        return f"{text_part} {' , '.join(links)}"  # Возвращаем "знаками" + ссылки

    # Сначала заменяем разметку
    value = re.sub(marking_pattern, replace_marking, value)

    # Затем заменяем знаки с текстовой частью
    value = re.sub(sign_with_text_pattern, replace_sign_numbers, value)

    return mark_safe(value)



# from django import template
# import re
# from django.utils.safestring import mark_safe
# from urllib.parse import quote
#
# register = template.Library()
#
#
# @register.filter
# def linkify_markings(value, args):
#     """Автоматически превращает номера разметки и знаков в ссылки с картинками."""
#
#     # Обработка аргументов
#     if isinstance(args, str):
#         try:
#             args = dict(arg.split('=') for arg in args.split(','))
#         except ValueError:
#             args = {'topic_id': '34', 'category_id': 'default_category'}
#
#     topic_id = args.get('topic_id', '34')  # Убедись, что 34 — это тема разметки
#     category_id = args.get('category_id', 'default_category')
#
#     # Удаляем старые ссылки и изображения
#     value = re.sub(r'<a[^>]*>(.*?)</a>', r'\1', value)
#     value = re.sub(r'<img[^>]*>', '', value)
#
#     # Паттерн для разметки (например, 1.1.1, 1.2.3)
#     # marking_pattern = r'\b\d{1,2}\.\d{1,2}\.\d{1,2}\b'
#     marking_pattern = r'\b(?:лінію|розмітку)\s+(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\b'
#
#     # Паттерн для знаков (например, 1.1, 1.2)
#     sign_pattern = r'\b\d{1,2}\.\d{1,2}\b'
#
#     def replace_marking(match):
#         marking_number = match.group(1)
#         encoded_marking_number = quote(marking_number, safe="")
#
#         link = f'<a href="/topic/{topic_id}/categories/{category_id}/markings/{marking_number}/">{marking_number}</a>'
#         image = f'<img src="/media/markings/{encoded_marking_number}.webp" class="markings-image">'
#
#         return f'{link} {image}'
#
#     def replace_sign(match):
#         sign_number = match.group(0)
#         encoded_sign_number = quote(sign_number, safe="")
#
#         sign_link = f'<a href="/topic/{topic_id}/categories/{category_id}/signs/{sign_number}/">{sign_number}</a>'
#         sign_image = f'<img src="/media/sign/{encoded_sign_number}.webp" class="sign-image">'
#
#         return f'{sign_link} {sign_image}'
#
#     # Сначала заменяем ссылки на разметку
#     value = re.sub(marking_pattern, replace_marking, value)
#
#     # Затем заменяем ссылки на знаки
#     value = re.sub(sign_pattern, replace_sign, value)
#
#     return mark_safe(value)