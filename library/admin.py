from .models import Book, Genre, Author, SharedBook, followSystem
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

@admin.register(SharedBook)
class SharedBookAdmin(admin.ModelAdmin):
    list_display = ['borrower', 'book', 'shared_on_date', 'shared_until']

@admin.register(followSystem)
class followSystemAdmin(admin.ModelAdmin):
    list_display = ['this_user']

