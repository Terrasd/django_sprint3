from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'

admin.site.unregister(Group)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_select_related = ('category', 'location')
    list_display = (
        'title',
        'pub_date',
        'category',
        'is_published'
    )
    list_editable = (
        'is_published',
    )
    list_filter = ('category',)
    search_fields = ('title__startswith',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'is_published'
    )
    list_editable = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
