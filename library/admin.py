from .models import Book, Genre, Author, requestBook, followSystem
from django.contrib import admin


# Register your models here.

@admin.register (Book)
class BookAdmin (admin.ModelAdmin):
    list_display = ['title', 'slug', 'available', 'author']
    list_filter = ['available', ]
    prepopulated_fields = {'slug': ('title',)}


@admin.register (Author)
class AuthorAdmin (admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'slug']
    list_filter = ['last_name']
    prepopulated_fields = {'slug': ('last_name',)}


@admin.register (Genre)
class GenreAdmin (admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register (requestBook)
class RequestBookAdmin (admin.ModelAdmin):
    list_display = ['borrower', 'shared_on_date', 'shared_until']
    fieldsets = (
        (
            'Fields', {
                'fields': (
                    'books',)
            },
        ),
    )


@admin.register (followSystem)
class followSystemAdmin (admin.ModelAdmin):
    list_display = ['this_user']
