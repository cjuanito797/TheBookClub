from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from . import views

app_name = 'library'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:genre_slug>/', views.book_list, name='books_list_by_genre'),
    path('authors/', views.author_list, name='author_list')
]
