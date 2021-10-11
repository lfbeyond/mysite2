"""first_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#import xadmin
from django.contrib import admin
from django.conf.urls import  include, url
from blog import views
import django.contrib.auth.views
from mysite.settings import MEDIA_ROOT
from django.views.static import serve
#新的富文本mdeditor
from django.conf.urls import  include, url
from django.conf.urls.static import static
from django.conf import settings
#新的富文本mdeditor

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'admin/',admin.site.urls),
    url(r'^$',views.post_list,  name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/(?P<user_sigin>[0-9]+)/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^archives/$', views.archives, name='archives'),
    url(r'^tag/tag(?P<tag>\w+)/$', views.search_tag, name='search_tag'),
    url(r'^aboutme/$', views.about_me, name='about_me'),
    #url(r'^accounts/login/$',django.contrib.auth.views.LoginView, name='login'),
    url(r'^accounts/logout/$', django.contrib.auth.views.LogoutView, name='logout', kwargs={'next_page': '/'}),
    url(r'^search/$', views.blog_search, name='search'),
    url(r'^user/user(?P<user_id>\w+)/$', views.search_user, name='search_user'),
    url(r'^date/(?P<y>[0-9]{4})/(?P<m>[0-9]{1,2})$', views.search_date, name='search_date'),
    url(r'^register$', views.register_view,name='register'),
    url(r'^login$', views.login_view,name='login'),
    #url(r'^post/(?P<pk_post>[0-9]+)/$', views2.post_comment, name='post_comment'),
    url(r'', include('comments.urls',namespace="comments")),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    #url(r'^xadmin/', xadmin.site.urls)
    url(r'^media/(?P<path>.*)$',  serve,{"document_root": MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  ## 没有这一句无法显示上传的图片




# if settings . DEBUG :
#      # static files (images, css, javascript, etc.)
#      urlpatterns += static ( settings . MEDIA_URL , document_root = settings . MEDIA_ROOT )