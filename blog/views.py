from django.shortcuts import render

import sys,io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# Create your views here.
from django.shortcuts import render
from .models import *
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from .commons import cache_manager
from django.contrib.auth.decorators import login_required
import markdown2,markdown
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from comments.forms import CommentForm


from django.conf import settings
#redis缓存，关闭不用了.懒得装redis服务器
#from django.views.decorators.cache  import  cache_page
from django.contrib import messages

#@cache_page(60)
def post_list(request):
    postsAll = Article.objects.values('id','title','author','author_name','category','published_date').annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by('-published_date')
    #postsAll = Article.objects.annotate(num_comment=Count('id')).filter(published_date__isnull=False).order_by('-published_date')
    tags,date_list2=get_tags()
    for p in postsAll:
        p['click'] = cache_manager.get_click(p)
        p['category'] = p['category'].split()
        p['pk']=p['id']
        p['author_id']=p['author']
    # paginator = Paginator(postsAll, 5)  # Show 10 contacts per page
    # page = request.GET.get('page')
    print('-----------------------------')
    current_page = request.GET.get('page')
    if not current_page:
        current_page=int(1)
    #print(current_page)
    paginator=myPaginator(current_page,5,postsAll,5)
    posts = []
    print(paginator.max_pager_num)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
#    finally:
#         for pp in posts:
#             # pp.text = markdown.markdown(pp.text, extras=[
#             #                          'markdown.extensions.extra',
#             #                          'markdown.extensions.codehilite',
#             #                          'markdown.extensions.toc',
#             #                       ] )
#             print(pp.text)
#             pp['user']=pp['author']
    print(paginator.page_num_range())
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': True,'tags':tags,'date_list':date_list2})

from django.shortcuts import render, get_object_or_404
import re

#@cache_page(60)
def post_detail(request, pk):
    tags,date_list2= get_tags()
    #date_list2 = date_list()
    post = get_object_or_404(Article, pk=str(pk))
    #print(post.id)
    #print("------------------post_detail")
    #post.text = markdown.markdown(post.text.replace("\r\n",' \n'),extensions=[
    post.text = markdown.markdown(post.text,
                            extensions=[        
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ] )
    post.user=post.author
    post.category=post.category.split()
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()
    #print(comment_list)

    if post.published_date == None:
        return render(request, 'blog/post_detail.html',
                      {'post': post, 'comment_list': comment_list, 'form': form,'tags':tags,'date_list':date_list2})
    else:
        print("------------------post_detail3")
        postsAll = Article.objects.values('id','title').filter(
            published_date__isnull=False).order_by('-published_date')
        page_list = list(postsAll)
        print(page_list)
        if post.id == page_list[-1]['id']:
             print(post.id)
             try:
                before_page = page_list[-2]
             except:
                 before_page = None
             after_page = None
        elif post.id == page_list[0]['id']:
             #print(post)
             before_page = None
             after_page = page_list[1]
        else:
             #print(post.id)
             p_list=[]
             for i in page_list:
                 p_list.append(i['id'])
             situ = p_list.index(post.id)
             before_page = page_list[situ-1]
             after_page = page_list[situ+1]
        print("------------------- %s" %before_page )
        return render(request, 'blog/post_detail.html',
                      {'post': post, 'before_page': before_page, 'after_page': after_page,'comment_list': comment_list,'form': form,'tags':tags,'date_list':date_list2})

from .forms import ArticleForm
from django.shortcuts import redirect
@login_required
@csrf_exempt
def post_new(request):
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ArticleForm()
    return render(request, 'blog/post_edit.html', {'form': form,'tags':tags,'date_list':date_list2})




#@cache_page(60)
def post_draft_list(request,user_sigin):
    posts = Article.objects.filter(published_date__isnull=True).filter(author_id=user_sigin).order_by('-created_date')
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    for pp in posts:
        pp.category = pp.category.split()
    return render(request, 'blog/post_draft_list.html', {'posts': posts,'tags':tags,'date_list':date_list2})

def post_publish(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_edit(request, pk):
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    post = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = ArticleForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'tags':tags,'date_list':date_list2})

def post_remove(request, pk):
    post = get_object_or_404(Article, pk=pk)
    post.delete()
    return redirect('post_list')

from django.http import Http404

#@cache_page(60)
def archives(request):
    tags,date_list2=get_tags()
    try:
        post_list = Article.objects.values('id','title','author','author_name','published_date').filter(published_date__isnull=False).order_by('-published_date')
        post_list2=[]
        for a in post_list:
            a['user'] = a['author']
    except Article.DoesNotExist:
        raise Http404


    return render(request, 'blog/archives.html',
                  {'post_list': post_list, 'error': False, 'tags': tags, 'date_list': date_list2})



def search_tag(request, tag):
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    try:
        post_list = Article.objects.values('id','category','title','author','author_name','published_date').filter(category__icontains=tag).filter(published_date__isnull=False).order_by('-published_date')
        for pp in post_list:
            pp['category'] = pp['category'].split()
            #pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
            print("tag-------------- %s" %date_list2)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/tag.html', {'post_list' : post_list,'tags':tags,'date_list':date_list2})

#@cache_page(60)
def about_me(request):
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    return render(request, 'blog/aboutme.html',{'tags':tags,'date_list':date_list2})

from django.db.models import Q
def blog_search(request):
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    if 's' in request.GET:
        s = request.GET['s']
        print('search-----------------------------------------')
        print(s)
        if not s:
            messages.success(request, '搜索不能为空哦！.')
            return render(request, 'blog/search.html', {'error': 'ture','message':messages})
        else:
            post_list = Article.objects.values('id','category','title','author','author_name','published_date').filter(category__icontains=s).order_by('-published_date')
            if len(post_list) == 0 :
                messages.success(request, "sorry！没有搜索到相关内容！")
                return render(request, 'blog/search.html', {'error': 'ture','message':messages})
            else:
                for pp in post_list:
                    #pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
                    pp['category'] = pp['category'].split()
                return render(request, 'blog/search.html', {'post_list': post_list, 'error': False,'tags':tags,'date_list':date_list2})

    return redirect('/')

def search_user(request, user_id):
    tags,date_list2=get_tags()
    print(user_id)
    try:
        post_list = Article.objects.values('id','title','category','author','author_name','published_date').filter(author_id=user_id).filter(published_date__isnull=False).order_by('-published_date')
        for pp in post_list:
            pp['category']=pp['category'].split()
            #pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/search_user.html', {'post_list' : post_list,'tags':tags,'date_list':date_list2})

def search_date(request,y,m):
    tags,date_list2=get_tags()
    #date_list2 = date_list()
    print("----------------------------------------------")
    print(y,m)
    try:
        post_list = Article.objects.values('id','title','category','published_date').filter(published_date__isnull=False).order_by('-published_date')
        #print(post_list)
        post_list2 = []
        for pp in post_list:
            if str(pp['published_date'].year) == y and str(pp['published_date'].month) == m:
                pp['category']=pp['category'].split()
                #pp.text = markdown2.markdown(pp.text, extras=['fenced-code-blocks'], )
                post_list2.append(pp)
                print("+++++++++++++++++++++++++++%s " %post_list2)
            else:
                print(pp['published_date'].year)
                print(pp['published_date'].month)
    except Article.DoesNotExist:
        raise Http404

    return render(request, 'blog/date_list.html', {'post_list' : post_list2 ,'tags':tags,'date_list':date_list2})





from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
# 第四个是 auth中用户权限有关的类。auth可以设置每个用户的权限。

from .forms import UserForm

#注册
@csrf_exempt
def register_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 判断用户是否存在
            user = auth.authenticate(username = username,password = password)
            if user:
                print('=========================================================')
                context['userExit']=True
                return render(req, 'blog/register.html', context)


            #添加到数据库（还可以加一些字段的处理）
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #添加到session
            req.session['username'] = username
            #调用auth登录
            auth.login(req, user)
            #重定向到首页
            return redirect('/')
    else:
        context = {'isLogin':False}
    #将req 、页面 、以及context{}（要传入html文件中的内容包含在字典里）返回
    return  render(req,'blog/register.html',context)

#登陆
@csrf_exempt
def login_view(req):
    context = {}
    if req.method == 'POST':
        form = UserForm(req.POST)
        if form.is_valid():
            #获取表单用户密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #print(username,password)

            #获取的表单数据与数据库进行比较
            user = authenticate(username = username,password = password)
            if user:
                #比较成功，跳转index
                auth.login(req,user)
                req.session['username'] = username
                return  redirect('/')
            else:
                #比较失败，还在login
                context = {'isLogin': False,'pawd':False}
                return render(req, 'blog/login.html', context)
    else:
        context = {'isLogin': False,'pswd':True}
    return render(req, 'blog/login.html', context)

#登出
def logout_view(req):
    #清理cookie里保存username
    auth.logout(req)
    return redirect('/')


from collections import Counter
def get_tags(): #返回标签和发布时间列表
    postsAll = Article.objects.values('id','category','published_date').annotate(num_comment=Count('id')).filter(
        published_date__isnull=False).order_by('-published_date')
    #print(postsAll)
    tags = []
    for p in postsAll:
        if  str(p['category']) != '':
            for i in p['category'].split():
                tags.append(i)
        #[str(p.category) for p in postsAll if str(p.category) != '']
    tags_dict = Counter(tags)
    tags_dict2=dict(tags_dict)
    tags_dict3=sorted(tags_dict2.items(),key=lambda item:item[1],reverse=True)

    year_month_list = [(p['published_date'].year, p['published_date'].month) for p in postsAll]
    year_month_dict = Counter(year_month_list)
    date_list = [(key[0], key[1], year_month_dict[key]) for key in year_month_dict]
    date_list.sort(reverse=True)
    #print(tags_dict3,date_list)
    return tags_dict3,date_list

# def date_list():
#     postsAll = Article.objects.annotate(num_comment=Count('id')).filter(
#         published_date__isnull=False).order_by('-published_date')
#     year_month_list = [(p.published_date.year, p.published_date.month) for p in postsAll]
#     year_month_dict = Counter(year_month_list)
#     date_list = [(key[0], key[1], year_month_dict[key]) for key in year_month_dict]
#     date_list.sort(reverse=True)
#     return date_list


