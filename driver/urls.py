from django.urls import path
from django.conf.urls.static import static
from sitefordriver import settings
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('rules/', views.rules, name='rules'),
    path('tests/', views.tests, name='tests'),
    path('fines/', views.fines, name='fines'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    # path('news/<int:news_id>/', views.show_news, name='news'д
    # path('topic_one/', views.topic_one, name='topic_one')
    path('category/<int:cat_id>/', views.show_category, name='category'),

    path('topic/<int:topic_id>/categories/', views.sign_categories, name='sign_categories'),
    path('topic/<int:topic_id>/categories/<int:category_id>/', views.category_detail, name='category_detail'),
    path('topic/<int:topic_id>/categories/<int:category_id>/signs/<str:code>/', views.sign_detail, name='sign_detail'),

    path('topic/<int:topic_id>/categories/markings/', views.road_marking_categories, name='road_marking_categories'),
    path('topic/<int:topic_id>/categories/markings/<int:category_id>/', views.road_marking_category_detail, name='road_marking_category_detail'),
    path('topic/<int:topic_id>/categories/<int:category_id>/markings/<str:code>/', views.road_marking_details, name='road_marking_details'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)# чтобы разрешить доступ к загруженным изображениям в режиме отладки: