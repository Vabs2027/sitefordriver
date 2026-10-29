from django.db.models.functions import Cast
from django.db.models import FloatField as DjangoFloatField
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.db.models import F

from driver.models import Topic, TrafficSign, SignCategory, RoadMarking, MarkingCategory, Comment

menu = [{'title': 'ПДР', 'url_name': 'rules'},
        {'title': 'Тести', 'url_name': 'tests'},
        {'title': 'Штрафи', 'url_name': 'fines'},
        {'title': 'О нас', 'url_name': 'about'},
        {'title': 'Вхід', 'url_name': 'login'}
        ]


# rules = [
#     {'id': 1, 'title': 'Загальні положення', 'content': 'Новини', 'is_published': True, 'url_name': 'topic_one'},
#     {'id': 2, 'title': 'Обов`язки та права водіїв механічних транспортних засобів', 'content': 'Головні сттаті', 'is_published': True, 'url_name': 'num2'},
# ]


# data_db = [
#     {'id': 1, 'title': 'Новини', 'content': 'Новини', 'is_published': True},
#     {'id': 2, 'title': 'Закон про Поліцию', 'content': 'Головні сттаті', 'is_published': True}
# ]


cats_db = [
    {'id': 1, 'name': 'Новини'},
    {'id': 2, 'name': 'Закон Про Поліцію'},
    {'id': 3, 'name': 'Нові Закони та нововведення'},
]


# def index(request):
#     data = {'title': 'Головна сторінка',
#             'menu': menu,
#             # 'news': data_db,
#             'cat_selected': 0,
#             }
#     return render(request, 'driver/index.html', context=data)
def index(request):

    context = {
        'menu': menu,
        'cat_selected': 0
        }
    return render(request, 'driver/index.html', context)


def tests(request):
    return render(request, 'driver/tests.html', {'title': 'Пройти тести с ПДР', 'menu': menu})


def fines(request):
    return render(request, 'driver/fines.html', {'title': 'Штрафи', 'menu': menu})


def about(request):
    return render(request, 'driver/about.html', {'title': 'О нас', 'menu': menu})


def login(request):
    return render(request, 'driver/enter.html', {'title': 'Вхід в особистий кабінет', 'menu': menu})


def show_news(request, news_id):
    return HttpResponse(f'Новини с id = {news_id}')


def show_category(request, cat_id):
    data = {'title': 'Рубрика',
            'menu': menu,
            # 'news': data_db,
            'cat_selected': cat_id,
            }
    return render(request, 'driver/index.html', context=data)


def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)#тут вибираем только одну тему
    sections = topic.points.all()

    redirects = {
        33: 'sign_categories',  # Дорожные знаки
        34: 'road_marking_categories'  # Дорожная разметка
    }
    if topic_id == 33:  # Для дорожных знаков
        return redirect('sign_categories', topic_id=topic_id)

    if topic_id == 34:  # Для дорожных знаков
        return redirect('road_marking_categories', topic_id=topic_id)

    if topic_id in redirects:
        return redirect(redirects[topic_id])

    context = {
        'menu': menu,
        'topic': topic,
        'sections': sections,
        'topic_id': topic.id,
    }

    return render(request, 'driver/topic_detail.html', context)


def rules(request):
    topics = Topic.objects.all()  # Здесь множество тем

    context = {
        'menu': menu,
        'topics': topics
    }
    return render(request, 'driver/rules.html', context)


# def traffic_sign_detail(request, sign_id):#request - HTTP запрос
#     sign = get_object_or_404(TrafficSign, id=sign_id)
#
#     return render(request, 'driver/traffic_sign_detail.html', {'sign': sign, 'menu': menu})


def category_detail(request, topic_id, category_id):#request — это объект запроса, передаваемый Django, содержащий данные о HTTP-запросе (метод, параметры и т. д.)
    category = get_object_or_404(SignCategory, id=category_id)#получаем конкретную категорию по id
    signs = category.signs.all()  # Предполагается, что есть связь между категориями и знаками, получаем знаки данной категории
                                  # Используем related_name='signs'

    return render(request, 'driver/signs_category_detail.html',
                  {'category': category,
                   'signs': signs,
                   'menu': menu,
                   'topic_id': topic_id,
                   'category_id': category_id})


def sign_detail(request,  topic_id, category_id, code):
    sign = get_object_or_404(TrafficSign, code=code)# Здесь sign уже доступен как переменная, потому что мы передал его в контекст шаблона во view-функции.
    category = sign.category

    # Получаем все знаки текущей категории
    signs_in_category = TrafficSign.objects.filter(category=category)

    # Кастомная сортировка по числовым значениям частей кода
    def custom_sort(sign):
        parts = sign.code.split('.')
        return tuple(int(part) for part in parts if part.isdigit())

    # Применяем сортировку
    sorted_signs = sorted(signs_in_category, key=custom_sort)

    # Ищем текущий знак по его позиции в отсортированном списке
    current_index = None
    for index, s in enumerate(sorted_signs):
        if s.code == sign.code:
            current_index = index
            break

    if current_index is None:
        return render(request, 'driver/error.html', {
            'message': "Знак не найден в списке категории.",
            'menu': menu,
        })

    # Предыдущий знак
    previous_sign = sorted_signs[current_index - 1] if current_index > 0 else None

    # Следующий знак
    next_sign = sorted_signs[current_index + 1] if current_index < len(sorted_signs) - 1 else None

    return render(request, 'driver/sign_detail.html', {
        'sign': sign,
        'menu': menu,
        'category': category,
        'next_sign': next_sign,
        'previous_sign': previous_sign,
        'topic_id': topic_id,
        'category_id': category_id,
    })


def sign_categories(request, topic_id):
    categories = SignCategory.objects.all()

    return render(request, 'driver/sign_categories.html',
                  {'categories': categories,
                   'menu': menu,
                   'topic_id': topic_id})


def road_marking_categories(request, topic_id):#список всех категорий
    categories = MarkingCategory.objects.all()  # Получаем все категории разметки


    return render(request, 'driver/road_marking_categories.html',
                  {'categories': categories,
                   'menu': menu,
                   'topic_id': topic_id,
                   })


def road_marking_category_detail(request, topic_id, category_id):
    category = MarkingCategory.objects.get(id=category_id)
    markings = RoadMarking.objects.filter(category=category)  # Получаем все разметки для данной категории

    return render(request, 'driver/road_marking_category_detail.html',
                  {'category': category,
                   'markings': markings,
                   'topic_id': topic_id,
                   'category_id': category_id})


def road_marking_details(request, topic_id, category_id, code):
    # Получаем текущую категорию и разметку
    category = get_object_or_404(MarkingCategory, id=category_id)
    marking = get_object_or_404(RoadMarking, code=code, category=category)

    # Все разметки в текущей категории
    markings_in_category = RoadMarking.objects.filter(category=category)

    # Кастомная сортировка по числовым значениям частей кода
    def custom_sort(item):
        parts = item.code.split('.')
        return tuple(int(part) for part in parts if part.isdigit())

    # Применяем сортировку
    sorted_markings = sorted(markings_in_category, key=custom_sort)

    # Ищем текущую разметку в отсортированном списке
    current_index = None
    for index, m in enumerate(sorted_markings):
        if m.code == marking.code:
            current_index = index
            break

    if current_index is None:
        return render(request, 'driver/error.html', {
            'message': "Розмітки не знайдено в цій категорії.",
            'menu': menu,
        })

    # Предыдущая и следующая разметки
    previous_marking = sorted_markings[current_index - 1] if current_index > 0 else None
    next_marking = sorted_markings[current_index + 1] if current_index < len(sorted_markings) - 1 else None

    return render(request, 'driver/road_marking_details.html', {
        'menu': menu,
        'category': category,
        'marking': marking,
        'previous_marking': previous_marking,
        'next_marking': next_marking,
        'topic_id': topic_id,
    })




def page_not_found(request, exception):
    return HttpResponseNotFound('СТраница не найдена')
