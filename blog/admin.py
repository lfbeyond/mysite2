from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib import admin
from .models import Article
admin.site.register(Article)

class BlogAdmin(object):
    style_fields = {'text': 'ueditor'}