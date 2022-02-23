from django.shortcuts import render
from .models import Genre, Book, Author
from accounts.views import Signup


# Create your views here.
# Create your views here.
def book_list(request, genre_slug=None):
    genre = None
    genres = Genre.objects.all ( )
    books = Book.objects.filter (available=True)

    if genre_slug:
        genre = get_object_or_404 (Genre, slug=genre_slug)
        books = books.filter (genre=genre)

    return render (request,
                   'library/books/list.html',
                   {
                       'genres': genres,
                       'genre': genre,
                       'books': books
                   })


def book_detail(request, id, slug):
    book = get_object_or_404 (Book,
                              id=id,
                              slug=slug,
                              available=True)
    return render (request,
                   'library/books/detail.html',
                   {
                       'book': book,

                   })


def author_detail(request, id, slug):
    author = get_object_or_404 (Author,
                                id=id,
                                slug=slug)
    return render (request,
                   'library/author/authorDetail.html',
                   {
                       'author': author,
                   })


def author_list(request):
    authors = Author.objects.all ( )

    return render (request,
                   'library/author/authorList.html',
                   {
                       'authors': authors
                   })


def home(request):
    return render (request, 'home.html')