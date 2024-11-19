from symbol import namedexpr_test

from django.urls import path
from blog import views
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView
urlpatterns = [
    #首页
    path('', views.index,name='index'),
    #文章详情页
    path('article/<int:id>/',views.article_detail,name='article_detail'),
    #成员页
    path('member/',views.member,name='member'),
    #分类和标签页
    path('category_tag/',views.category_tag,name='category_tag'),
    #文章分类详情页
    path('article_category/(?P<id>[0-9]+)$',views.article_category,name='article_category'),
    #文章标签详情页
    path('article_tag/<int:id>',views.article_tag,name='article_tag'),
    #关于
    path('about/', views.about, name='about'),

    #文章归档
    path('article_set/<int:id>',views.article_set,name='article_set'),
    path('article_year/',views.article_year,name='article_year'),


    path('category/',views.category,name='category'),
    path('tag/',views.tag,name='tag'),

    path('cloud_tag/',views.cloud_tag,name='cloud_tag'),
    path('search/',views.search,name='search'),

    path('archive2/<int:id>',views.archive2,name='archive2'),

    path('echarts_category/',views.echarts_category,name='echarts_category'),
    path('echarts_activate/', views.echarts_activate, name='echarts_activate'),
    path('echarts_city/',views.echarts_city,name='echarts_city'),

    #留言板
    path('message/',views.message,name='message'),
    path('friend/',views.friend,name='friend')

]

#mkeditor配置
from django.conf.urls.static import static
from django.conf import settings
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)