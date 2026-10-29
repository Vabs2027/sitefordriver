from django import template
import driver.views as views

register = template.Library()

@register.simple_tag()#пользовательский тег
def get_categories():
    return views.cats_db


@register.inclusion_tag('driver/list_categories.html')#включающейся тег
def show_categories(cats_selected=0):#етот тег возвращает html стр - list_categories, cat_selected - для подстветки ссылки
    cats = views.cats_db
    return {'cats': cats, 'cat_selected': cats_selected}