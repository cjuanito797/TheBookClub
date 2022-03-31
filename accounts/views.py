from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm, LoginForm, EditAddress
from django.contrib.auth.decorators import login_required
from library.models import Book, Author, Genre
from .forms import *


# Create your views here.
class registration_view (FormView):
    def post(self, request):
        form = RegistrationForm (request.POST)

        if form.is_valid ( ):
            form.save ( )
            return redirect (reverse ('accounts:user_login'))
        return render (request, 'registration/register.html', {'form': form})

    def get(self, request):
        form = RegistrationForm ( )
        return render (request, 'registration/register.html', {'form': form})


def user_login(request):
    form = LoginForm (request.POST)
    if form.is_valid ( ):
        cd = form.cleaned_data
        user = authenticate (request,
                             username=cd['email'],
                             password=cd['password'])
        if user is not None:
            if user.is_active:
                login (request, user)
                return render (redirect ('accounts:customerView'))
            else:
                return HttpResponse ('Disabled Account')
        else:
            return HttpResponse ('Invalid Login')
    else:
        form = LoginForm ( )
    return render (request, 'registration/login.html', {'form': form})


@login_required
def customerView(request):
    favorite_books = Book.objects.filter(owner_id=request.user.id, favorite=True)

    return render (request, 'accounts/base.html', {'favorite_books': favorite_books})


@login_required
def myBookShelf(request):
    myBooks = Book.objects.filter (owner_id=request.user,).order_by("title")
    return render (request, 'accounts/myBookshelf.html', {'myBooks': myBooks})

@login_required
def editProfile(request):
    return render (request, 'profileCustomization/editProfile.html')

@login_required
def viewProfile(request, id):
    favBooks = Book.objects.filter(owner_id=request.user.id, favorite=True)
    return render (request, 'profileCustomization/viewProfile.html', {'user': user, 'favBooks': favBooks})

@login_required
def addBook(request):
    if request.method == "POST":
        addBook = addBookForm(request.POST)
        addAuthor = addAuthorForm(request.POST)
        addGenre = addGenreForm(request.POST)

        if addBook.is_valid() and addAuthor.is_valid() and addGenre.is_valid():
            user = request.user
            book = addBook.save(commit=False)
            book.owner_id = request.user.id
            author = addAuthor.save(commit=False)
            genre = addGenre.save(commit=False)
            book.author = author
            book.genre = genre
            author.save()
            genre.save()
            book.save()

            if book.favorite is True:
                user.favoriteAuthors.add(author)
                user.favoriteGenres.add(genre)


            return redirect(reverse('accounts:myBookShelf'))
    else:
        addBook = addBookForm ()
        addAuthor = addAuthorForm ()
        addGenre = addGenreForm ()
    return render(request, "accounts/addBook.html", {'addBook' : addBook, 'addAuthor': addAuthor, 'addGenre': addGenre})


@login_required
def user_logout(request):
    return HttpResponseRedirect (reversed ('your_app:login'))


@login_required
def edit_address(request):
    if request.method == "POST":
        form = EditAddress (request.POST or None, instance=request.user,use_required_attribute=False )
        if form.is_valid( ):
            form.save( )
            return render (request, 'profileCustomization/editProfile.html')

    else:
        form = EditAddress (request.POST or None, instance=request.user, use_required_attribute=False )
    return render (request, 'profileCustomization/editAddress.html', {'form': form})

@login_required()
def viewFavBooks(request):
    favBooks = Book.objects.filter (owner_id=request.user.id, favorite=True)

    return render (request, 'profileCustomization/myFavoriteBooks.html', {'favBooks': favBooks})



@login_required()
def viewFavAuthors(request):
    user = request.user
    favAuthors = user.favoriteAuthors.distinct()

    uniqueAuthors = []
    for fa in favAuthors:
        if fa not in uniqueAuthors:
            uniqueAuthors.append(fa)

    # now we will also get the favorite authors from the books that were marked as favorites again we will still want to keep it unique

    return render(request, 'profileCustomization/myFavoriteAuthors.html', {'uniqueAuthors': uniqueAuthors} )

@login_required()
def viewFavGenres(request):
    user = request.user
    favGenres = user.favoriteGenres.filter()
    uniqueGenres = []
    for fg in favGenres:
        if fg.name not in uniqueGenres:
            uniqueGenres.append(fg.name)

    return render(request, 'profileCustomization/myFavoriteGenres.html', {'uniqueGenres' : uniqueGenres})

@login_required()
def addFavAuthors(request):
    if request.method == "POST":
        favAuthor = addAuthorForm(request.POST)

        if favAuthor.is_valid():
            author = favAuthor.save(commit=False)
            author.favorite = True
            author.save()
    else:
        favAuthor = addAuthorForm(request.POST)

    return render(request, 'profileCustomization/addFavAuthor.html', {'favAuthor' : favAuthor})


@login_required()
def deleteBook(request, pk):
    # whenever we delete a book, we also want to go through and delete the related author as well as the related genre.
    book = get_object_or_404(Book, pk=pk)
    author = book.author
    genre = book.genre
    book.delete()
    author.delete()
    genre.delete()
    return redirect('accounts:myBookShelf')