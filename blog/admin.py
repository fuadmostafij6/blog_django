from django.contrib import admin

from .models import Post, Reply, Comment, Category


admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(Comment)
admin.site.register(Category)
