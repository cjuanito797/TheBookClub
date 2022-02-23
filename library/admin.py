from .models import Book, Genre, Author
from django.contrib import admin

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price', 'available', 'author']
    list_filter = ['available', ]
    prepopulated_fields = {'slug':('title', )}

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'slug']
    list_filter = ['last_name']
    prepopulated_fields = {'slug': ('last_name', )}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name', )}