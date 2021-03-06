from django.shortcuts import render, redirect, reverse
from .models import Genre, Book, Author
from accounts.views import registration_view
from django.urls import reverse_lazy
from .forms import BookForm
from bootstrap_modal_forms.generic import BSModalCreateView
from accounts.views import customerView
from django.contrib.auth.decorators import login_required

# Create your views here.


class BookCreateView(BSModalCreateView):
    template_name = "library/books/createBook.html"
    form_class = BookForm
    success_message = "Success: Book was created"
    success_url = reverse_lazy("library:home")


def book_list(request, genre_slug=None):
    genre = None
    genres = Genre.objects.all()
    books = Book.objects.all()

    if genre_slug:
        genre = get_object_or_404(Genre, slug=genre_slug)
        books = books.filter(genre=genre)

    return render(
        request,
        "library/books/list.html",
        {"genres": genres, "genre": genre, "books": books},
    )


def book_detail(request, id, slug):
    book = get_object_or_404(Book, id=id, slug=slug, available=True)
    return render(
        request,
        "library/books/detail.html",
        {
            "book": book,
        },
    )


def author_detail(request, id, slug):
    author = get_object_or_404(Author, id=id, slug=slug)
    return render(
        request,
        "library/author/authorDetail.html",
        {
            "author": author,
        },
    )


def author_list(request):
    authors = Author.objects.values("first_name", "last_name").distinct()

    return render(request, "library/author/authorList.html", {"authors": authors})


def home(request):

    if request.user.is_authenticated:
        return redirect(reverse("accounts:customerView"))
    else:
        return render(request, "home.html")


def contactus(request):
    return render(request, "contactus.html")

@login_required
def shareABook(request):
    books = Book.objects.all().filter(owner_id=request.user.id)
    return render(request, 'LibraryFunctions/shareBook.html', {'books' : books})
