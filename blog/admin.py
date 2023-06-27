from django.contrib import admin
from .models import Category, Comment, Post, Tag

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} 

admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "excerpt", "status",)
    prepopulated_fields = {"slug": ("title",)} 

admin.site.register(Post, PostAdmin)


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)} 

admin.site.register(Tag, TagAdmin)
admin.site.register(Comment)
