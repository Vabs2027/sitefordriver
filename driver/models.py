from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField
import os




#модель для тем
class Topic(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва теми')#verbose_name - для адмін панелі, а так он испол во многом!
    description = HTMLField(verbose_name='Зміст теми', blank=True, null=True)


    class Meta:
        verbose_name = 'Теми з ПДР'#admin panel
        verbose_name_plural = 'Теми з ПДР'#указ в ед числе (s)


    def __str__(self):
        return self.title


    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)


class TopicPoint(models.Model):
    topic = models.ForeignKey(Topic, related_name='points', on_delete=models.CASCADE, verbose_name='Тема')
    number = models.CharField(max_length=10, verbose_name='номер', blank=True, null=True)
    text = HTMLField(verbose_name='Текст самого пункту')
    # buttons_cust_filtr = models.CharField(max_length=100, verbose_name='Текст кнопки термина', blank=True, null=True)


    def __str__(self):
        return f'{self.number} - {self.text[:20]}...'


class TopicSection(models.Model):
    topic_point = models.ForeignKey(TopicPoint, related_name='sections', on_delete=models.CASCADE, verbose_name='Коментарі до пункту')
    description = HTMLField(verbose_name='Коментарі до пункту')
    image_section = models.ImageField(upload_to='image_section/', blank=True, null=True)


    class Meta:
        verbose_name = 'Коментарі до темы'  # admin panel
        verbose_name_plural = 'Коментарі до пункту'  # указ в ед числе (s)


    def __str__(self):
        if self.topic_point:
            return f'{self.topic_point.text} - {self.topic_point.number}'
        return 'Topic Section without a Point'


#модель для коментариев
class Comment(models.Model):
    section = models.ForeignKey(TopicSection, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    topics = models.ForeignKey(Topic, related_name='comments', on_delete=models.CASCADE, verbose_name='Назва теми')
    # author = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем, оставившим комментарий
    text = models.TextField(verbose_name='Коментарі до обранної теми')  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания комментария


    class Meta:
        verbose_name = 'Коментарі до кожної теми'#admin panel
        verbose_name_plural = 'Коментарі до кожної теми'#указ в ед числе (s)


    def __str__(self):
        # return f"Comment by {self.author.username} on {self.topic.title}"
        return self.text

# Модель для изображений, связанных с комментариями
class CommentImage(models.Model):
    comment = models.ForeignKey(Comment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comment_images/')  # Путь для загрузки изображений
    # caption = models.CharField(max_length=200, blank=True)  # Подпись к изображению (необязательно)


    def __str__(self):
        return self.image
        # return f"Image for comment {self.comment.id} by {self.comment.author.username}"
    


class SignCategory(models.Model):#модель категории дор знаков
    name = models.CharField(max_length=225, verbose_name='Категорії дорожніх знаків')
    description = models.TextField(blank=True, null=True, verbose_name='Опис дорожнього знака')


    class Meta:
        verbose_name = 'Категорії дорожніх знаків'#admin panel
        verbose_name_plural = 'Категорії дорожніх знаків'#указ в ед числе (s)


    def __str__(self):
        return self.name


def sign_upload_path(instance, filename):
    """Генерация пути для знаков (номер_знака.webp)"""
    base_name, ext = os.path.splitext(filename)
    new_name = f"{instance.code}{ext}"  # Просто номер знака без "rozkitka_"
    return os.path.join("signs/", new_name)


class TrafficSign(models.Model):#модель дорожного знака
    name = models.CharField(max_length=225, verbose_name='Назва дорожнього знака')
    code = models.CharField(null=True, max_length=10, verbose_name='Номер знака')  # Уникальный код знака
    sort_order = models.CharField(max_length=20)
    # topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='categories')  # Связь с моделью Topic
    # Другие поля категории знаков
    description = HTMLField(verbose_name='Опис знака', blank=True, null=True)#HTMLFiledдля форматирования (жирный текст, ссылки, картинки и т.д.).
    image = models.ImageField(upload_to=sign_upload_path, blank=True, null=True)
    category = models.ForeignKey(SignCategory, related_name='signs', verbose_name='Категорія знака', on_delete=models.CASCADE)
    related_signs = models.ManyToManyField('self', symmetrical=False, blank=True)#related_signs — это поле ManyToManyField, которое позволяет одному знаку ссылаться на другие знаки. Это поможет связать знаки между собой.
            #symmetrical=Falseуказывает на то, что отношения не являются симметричными.
            #'sef' - используется, когда модель ссылается на саму себя. Это позволяет установить связь между объектами одной и той же модели.
            #related_to — это обратная связь, которая позволяет узнать, какие знаки ссылаются на данный знак.
    real_life_image = models.ImageField(upload_to='real_life_images/', blank=True, null=True, verbose_name='Картинка из реал.жизни')  # Новое поле для других изобрж


    class Meta:
        verbose_name = 'Дорожній знак'#admin panel
        verbose_name_plural = 'Дорожній знак'#указ в ед числе (s)
        ordering = []


    def __str__(self):
        return self.name


    def full_name_code(self):
        return f'{self.code} {self.name}'


class MarkingCategory(models.Model):#модель категории дор разметки
    name = models.CharField(max_length=255, verbose_name='Категорія дорожньої розмітки')
    description = models.TextField(blank=True, null=True, verbose_name='Опис дорожньої розмітки')


    class Meta:
        verbose_name = 'Категорії дорожньої розмітки'#admin panel
        verbose_name_plural = 'Категорії дорожньої розмітки'


    def __str__(self):
        return self.name


def custom_upload_path(instance, filename):
    base_name, ext = os.path.splitext(filename)
    new_name = f"rozkitka_{instance.code}{ext}"
    print(f"Saving file: {new_name}")  # Выведет путь файла при его сохранении

    return os.path.join("markings/", new_name)


class RoadMarking(models.Model):#модель дорожной разметки
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True, verbose_name='Код розмітки', null=True, blank=True)  # Если код не обязателен
    category = models.ForeignKey(MarkingCategory, related_name='markings', verbose_name='Категорія', on_delete=models.CASCADE)
    description = HTMLField(verbose_name='Опис розмітки', blank=True)
    image = models.ImageField(upload_to=custom_upload_path, blank=True, null=True)
    real_life_image = models.ImageField(upload_to='real_life_images_marking/', blank=True, null=True, verbose_name='Картинка из реал.жизни')  # Новое поле для других изобрж


    class Meta:
        verbose_name = 'Дорожння розмітка'#admin panel
        verbose_name_plural = 'Дорожння розмітка'
        ordering = []


    def __str__(self):
        return self.name


    def full_name_code(self):
        return f'{self.code} {self.name}'



