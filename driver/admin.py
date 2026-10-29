from django.contrib import admin
from django.db.models import Func
from django.db.models import F, Func, Value, IntegerField
from tinymce.widgets import TinyMCE

from django.db import models
from .models import Topic, Comment, CommentImage, SignCategory, TrafficSign, MarkingCategory, RoadMarking, TopicSection, \
    TopicPoint


class TopicPointInline(admin.TabularInline):
    model = TopicPoint
    extra = 1  # Количество пустых форм для добавления новых записей


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')#отображение в админ панеле
    list_display_links = ('id', 'title')#для кликабельных полей
    ordering = ['id']#порядок сортивоки записей в админ панеле!
    inlines = [TopicPointInline]  # Добавляем Inline


# class CommentImageInline(admin.TabularInline):#TabularInLine-
#     model = CommentImage


@admin.register(TopicSection)
class TopicSectionAdmin(admin.ModelAdmin):
    list_display = ('topic_point', 'description', 'image_section')
    #  настраивать формы
    fields = ('topic_point', 'description', 'image_section')
    ordering = ['topic_point']



@admin.register(TopicPoint)
class TopicPointAdmin(admin.ModelAdmin):
    list_display = ('topic', 'number', 'text')
    #  настраивать формы
    fields = ('topic', 'number', 'text')
    ordering = ['topic', 'number']



# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     inlines = [CommentImageInline]#


@admin.register(SignCategory)
class SignCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    ordering = ['id']#порядок сортировки


@admin.register(TrafficSign)
class TrafficSignAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ('code', 'name', 'category', 'description')
    list_filter = ('category',)
    search_fields = ['code', 'name']
    # list_display = ('code', 'name', 'category', 'description')
    # list_filter = ('category',)  # фильтрация по категориям
    ordering = ['code']  # сортировка по полю "code" по возрастанию
    # search_fields = ['code', 'name']


    # def get_queryset(self, request):#используется для переопределения поведения выборки объектов модели
    #     queryset = super().get_queryset(request)
    #     sorted_list = sorted(queryset, key=lambda sign: sign.code_as_float)
    #     pks = [sign.pk for sign in sorted_list]
    #     return queryset.filter(pk__in=pks)


@admin.register(MarkingCategory)
class MarkingCategory(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(RoadMarking)
class RoadMarking(admin.ModelAdmin):
    list_display = ('code', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('code', 'name')




# admin.site.register(Topic, TopicAdmin)
# admin.site.register(Comment, CommentAdmin)

