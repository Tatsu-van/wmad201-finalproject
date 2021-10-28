from django.contrib import admin

# Register your models here.

from django.contrib import admin

from blog.models import Category, Tag, Post

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)