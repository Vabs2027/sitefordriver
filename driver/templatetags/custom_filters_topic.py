from django import template
import re
from django.utils.safestring import mark_safe
from driver.models import TopicPoint

register = template.Library()

@register.filter
def add_comment_buttons(value):
    """Добавляет кнопку с текстом из модели после окончания описания терминов."""

    # Берем все термины из пункта 1.10, у которых есть текст кнопки
    terms = TopicPoint.objects.filter(number="1.10", sections__isnull=False).exclude(sections__description="")


    # Создаем словарь {текст пункта: текст кнопки}
    term_dict = {term.text.strip(): term.sections.first().description for term in terms if term.sections.exists()}


    # Если нет подходящих терминов, сразу возвращаем оригинальный текст
    if not term_dict:
        return mark_safe(value)

    # Шаблон поиска терминов в тексте
    pattern = r'\b(' + '|'.join(map(re.escape, term_dict.keys())) + r')\b(.*?)([.:;])'

    def replace_match(match):
        term = match.group(1).strip()  # Сам термин (например, "автобус")
        text = match.group(2)  # Описание термина
        punctuation = match.group(3)  # Знак препинания в конце
        button_html = f' <button class="comment-btn">{term_dict[term]}</button>'  # Добавляем текст кнопки
        return f"{term}{text}{button_html}{punctuation}"

    # Выполняем замену
    new_value = re.sub(pattern, replace_match, value)
    return mark_safe(new_value)


