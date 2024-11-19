from calendar import day_abbr
from email.policy import default
from lib2to3.fixes.fix_input import context
from msilib import datasizemask
import json
import logging
import traceback
from tempfile import template
from venv import logger

from django.contrib.admin.templatetags.admin_list import result_list
from setuptools.package_index import unique_values

from blog.utils.Pagination import Pagination
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F, Q, Count
from wheel.cli import tags_f
from itertools import groupby, count
from .models import Article, Link, Category, Tag, Notice, Valine, About, Site, Social, Skill,Year,City
import mistune
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
import markdown
import datetime
from django.db.models.functions import ExtractMonth, TruncDate
from collections import defaultdict
def index(request):
    """首页展示"""
    # 取出所有博客文章
    all_articles = Article.objects.all().order_by('-add_time')
    # 取出要推荐的博客文章
    top_articles = Article.objects.filter(is_recommend=1)
    notices = Notice.objects.all()
    #首页分页功能
    # try:
    #     page = request.GET.get('page',1)
    # except PageNotAnInteger:
    #     page = 1
    # p = Paginator(all_articles,9,request=request)
    # all_articles = p.page(page)
    queryset = Pagination(request, all_articles)

    #需要传递给模板（templates）的对象
    context = {
        "page_string": queryset.html(),
        'all_articles':queryset.page_queryset,
        'top_articles': top_articles,
        'notices': notices
    }
    # render函数：载入模板，并返回context对象
    return render(request, 'index.html', context)


def article_detail(request, id):
    """文章详情页"""
    # 取出相应的文章
    article = Article.objects.get(id=id)
    # 增加阅读数
    article.click_count += 1
    article.save(update_fields=['click_count'])
    valine = Valine.objects.first()  # 取第一条数据
    # 前台mK解析
    mk = mistune.Markdown()
    output = mk(article.content)

    #获取当前文章的上一篇文章
    current_time = article.add_time
    before_article = Article.objects.filter(add_time__lt=current_time).order_by('-add_time').first()
    next_article = Article.objects.filter(add_time__gt=current_time).order_by('add_time').first()
    if before_article is None:
        before_article = article
    if next_article is None:
        next_article = article

    # 需要传递给模板的对象
    context = {
        'valine': valine,
        'article': article,
        'article_detail_html': output,
        'before_article':before_article,
        'next_article':next_article
    }
    # 载入模板，并返回context对象
    return render(request, 'article_detail.html', context)

def member(request):
    '''成员详情页'''
    links = Link.objects.all()
    context = {'links': links, }
    return render(request, 'member.html', context)

def archive2(request,id):
    year = Year.objects.filter(id=id).first()
    articles = Article.objects.filter(years__id=id).all()
    if not articles:
        return render(request, 'archive2.html', {
            'artilces': None,
            "year": year.year,
        })
    articles = Pagination(request, articles)
    # 需要传递给模板（templates）的对象

    articles_list = {}
    for article in articles.page_queryset:
        articles_list[article.add_time.month] = []
    for article in articles.page_queryset:
        articles_list[article.add_time.month].append(article)
    context = {
         "articles": articles_list,
         "year": year.year,
         "page_string": articles.html(),
         'all_articles': articles.page_queryset,
    }
    return render(request, 'archive2.html',context)

def article_year(request):
    year_list = Year.objects.all()
    return render(request,'article_year.html',{"article":year_list})

def article_set(request,id):
    all_articles = Article.objects.filter(years__id=id).all().order_by('-add_time')
    if not all_articles:
        return render(request, 'archive.html', {
            'all_articles': None,
        })

    all_date = all_articles.values('add_time')
    latest_date = all_date[0]['add_time']
    all_date_list = []
    for i in all_date:
        all_date_list.append(i['add_time'].strftime("%Y-%m-%d"))

    # 遍历1年的日期
    end = datetime.date(latest_date.year, latest_date.month, latest_date.day)
    begin = datetime.date(latest_date.year - 1, latest_date.month, latest_date.day)
    d = begin
    date_list = []
    temp_list = []

    delta = datetime.timedelta(days=1)
    while d <= end:
        day = d.strftime("%Y-%m-%d")
        if day in all_date_list:
            temp_list.append(day)
            temp_list.append(all_date_list.count(day))
        else:
            temp_list.append(day)
            temp_list.append(0)
        d += delta
        date_list.append(temp_list)
        temp_list = []

    # 文章归档分页
    try:
        page = request.GET.get('page', 1)
    except PageNotAnInteger:
        page = 1

    p = Paginator(all_articles, 10, request=request)
    articles = p.page(page)

    return render(request, 'archive.html', {
        'all_articles': articles,
        'date_list': date_list,
        'end': str(end),
        'begin': str(begin),
    })
def category_tag(request):
    '''分类和标签页'''
    categories = Category.objects.all()
    tags = Tag.objects.all()
    context = {
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'category_tag.html', context)

def category(request):
    #返回分类
    categories = Category.objects.all()
    return render(request,'category_article.html',{"categories":categories})

def tag(request):
    #返回标签分类
    tags = Tag.objects.all()
    return render(request,'cartegory_tag.html',{"tags":tags})

def search(request):
    try:
        json_data = json.loads(request.body.decode())
        search_key = json_data.get("searchKey")
        if not search_key:
            return JsonResponse({"code": 400, "data": "Not searchKey", "msg": "fail"})
        page = json_data.get("page", 1)
        if page <= 0:
            page = 1
        page_size = json_data.get("pageSize", 10)
        page = int(page)
        page_size = int(page_size)
    except Exception as e:
        logger.info(traceback.format_exc())
        return JsonResponse({"code": 400, "data": None, "msg": "fail"})


    # 查询标题里面的含有关键字的
    article_list = Article.objects.values("title", "desc", "id", "add_time","author","click_count","category__name").order_by("add_time").filter(
        Q(title__icontains=search_key) | Q(content__icontains=search_key)).all()
    total_count = article_list.count()
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1
    if page >total_page_count:
        page = total_page_count
    # 分页
    article_paginator = Paginator(article_list, page_size)
    article_list = article_paginator.page(page).object_list
    return JsonResponse(
        {
            "code": 200,
            "data": {
                "articleList": list(article_list),
                "total_count":total_count,
                "pageInfo": {
                    "pageCount": article_paginator.num_pages,
                    "articleCount": article_paginator.count,
                    "currentPage": page,
                }
            },
            "msg": "success"
        }
    )


#留言板
def message(request):
    return  render(request,'message.html')

def member(request):
    link_list = Link.objects.all()
    return render(request, 'member.html', {"links": link_list})

def friend(request):
    link_list = Link.objects.all()

    return render(request,'friend.html',{"links":link_list})

def cloud_tag(request):
    # 返回云标签数据
    tags = Tag.objects.all()
    data = []
    for tag in tags:
        data.append({"text": tag.name, "weight": 1, "link": "/article_tag/"+ str(tag.id)})
    result = {
        "status": True,
        "data": data,
    }
    return JsonResponse(result, safe=False)

def article_category(request, id):
    '''文章分类详情页'''
    categories = Category.objects.all()
    articles = Category.objects.get(id=id).article_set.all()  # 获取该id对应的所有的文章
    queryset = Pagination(request,articles,page_size=6)
    context = {
        "page_string": queryset.html(),
        'categories': categories,
        'id': id,
        'articles': queryset.page_queryset
    }
    return render(request, 'article_category.html', context)


def article_tag(request, id):
    '''文章标签详情页'''
    tags = Tag.objects.all()
    articles = Tag.objects.get(id=id).article_set.all()
    queryset = Pagination(request, articles, page_size=6)
    context = {
        'tags': tags,
        'id': id,
        'articles': queryset.page_queryset,
        "page_string": queryset.html(),
    }
    return render(request, 'article_tag.html', context)


def add_nav(request):
    '''导航栏'''
    category_nav = Category.objects.filter(add_menu=True).order_by('index')
    context = {
        'category_nav': category_nav,
    }
    return render(request, 'layout/header.html', context)


def about(request):
    articles = Article.objects.all().order_by('-add_time')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    about = About.objects.first()
    skill = Skill.objects.all()
    return render(request, 'about.html', {
        'articles': articles,
        'categories': categories,
        'tags': tags,
        'about': about,
        'skill': skill,
    })


def echarts_city(request):
    city_list = City.objects.all()
    temp = []
    for city in city_list:
        dict = {
            "name":city.name,
            "value":city.value
        }
        temp.append(dict)
        result = {
            "status":True,
            "data":{
                "data_list":temp
            }
        }
    return JsonResponse(result)


def echarts_category(request):
    data_list = []
    catagroy_list = Category.objects.all()
    catagroy_count = Category.objects.count()
    for catagory in catagroy_list:
        dict = {}
        count = Article.objects.filter(category_id=catagory.id).count()
        dict["value"] = count
        dict["name"] = catagory.name
        data_list.append(dict)
    result = {
        "status":True,
        "data":{
            "data_list":data_list,
            "count":catagroy_count
        }
    }
    return JsonResponse(result)


def echarts_activate(request):
    article_by_day = Article.objects.annotate(
        day = TruncDate('add_time')
    ).values('day').annotate(
        article_count = Count('id')
    ).order_by('-day')[0:10]
    datalist = []
    valuelist = []
    for group in article_by_day:
        datalist.append(group['day'].strftime('%Y-%m-%d'))
        valuelist.append(group['article_count'])
    datalist = datalist[::-1]
    valuelist = valuelist[::-1]
    result = {
        "status":True,
        "data":{
            "datalist":datalist,
            "valuelist":valuelist
        }
    }
    return JsonResponse(result)

def global_params(request):
    """全局变量"""
    # 分类是否增加到导航栏
    category_nav = Category.objects.filter(add_menu=True).order_by('index')
    site_name = Site.objects.first().site_name
    logo = Site.objects.first().logo
    keywords = Site.objects.first().keywords
    desc = Site.objects.first().desc
    slogan = Site.objects.first().slogan
    dynamic_slogan = Site.objects.first().dynamic_slogan
    bg_cover = Site.objects.first().bg_cover
    icp_number = Site.objects.first().icp_number
    icp_url = Site.objects.first().icp_url
    social = Social.objects.all()
    return {
        'category_nav': category_nav,
        'SITE_NAME': site_name,
        'LOGO': logo,
        'KEYWORDS': keywords,
        'DESC': desc,
        'SLOGAN': slogan,
        'DYNAMIC_SLOGAN': dynamic_slogan,
        'BG_COVER': bg_cover,
        'ICP_NUMBER': icp_number,
        'ICP_URL': icp_url,
        'social': social,
    }

