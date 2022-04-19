import datetime
import email
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import User, Message, Post, PostComment, Reply
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm, LoginForm, EditAddress, messageForm
from django.contrib.auth.decorators import login_required
from library.models import Book, Author, Genre
from .forms import *
from django.db.models import Q
from library.models import followSystem
from django.contrib import messages


# Create your views here.
class registration_view (FormView):
    def post(self, request):
        form = RegistrationForm (request.POST, files=request.FILES)

        if form.is_valid ( ):
            form.save ( )
            return redirect (reverse ('accounts:user_login'))
        return render (request, 'registration/register.html', {'form': form})

    def get(self, request):
        form = RegistrationForm (files=request.FILES)
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
    if request.method == "POST":
        new_post = PostCreation (request.POST)
        if new_post.is_valid ( ):
            this = new_post.save (commit=False)
            this.writer_id = request.user.id
            this.save ( )

            return HttpResponseRedirect (request.path_info)



    else:
        new_post = PostCreation ( )

    favorite_books = Book.objects.filter (owner_id=request.user.id, favorite=True)
    allAvailableBooks = Book.objects.all ( ).exclude (owner_id=request.user.id)[0:3]
    my_posts = Post.objects.all ( ).filter (writer_id=request.user.id)

    this_user = User.objects.get (pk=request.user.id)
    list = this_user.follow_list.all ( )

    # for each person in the list get their posts
    post = 0
    posts = my_posts
    for item in list:
        post = Post.objects.all ( ).filter (writer_id=item.id).order_by ('-created_on')
        posts = post | posts

    posts.order_by ('-created_on')
    news_feed = dict()

    for p in posts:
        news_feed[p] = [p]

        # get the comments relating to the said post
        comments = PostComment.objects.all().order_by('created_on')



    return render (request, 'accounts/base.html',
                   {'avail_books': allAvailableBooks, 'favorite_books': favorite_books, 'posts': posts,
                    'new_post': new_post, 'comments' : comments})


@login_required
def search_results(request):
    input = request.GET.get ("input")
    results = Book.objects.filter (Q (title__icontains=input) | Q (author__first_name__icontains=input) | Q (
        author__last_name__icontains=input) | Q (genre__name__icontains=input))
    results.filter (available=True)
    results_found = results.exists ( )
    if (not results_found):
        results = Book.objects.filter (available=True)[:5]
    return render (request, 'accounts/search_results.html', {'results_found': results_found, 'results': results})


@login_required
def myBookShelf(request):
    myBooks = Book.objects.filter (owner_id=request.user, ).order_by ("title")
    return render (request, 'accounts/myBookshelf.html', {'myBooks': myBooks})


@login_required
def editProfile(request):
    if request.method == "POST":
        form = EditProfile (data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid ( ):
            form.save ( )
            return customerView (request)
    else:
        form = EditProfile (instance=request.user)
    return render (request, 'profileCustomization/editProfile.html', {'form': form})


@login_required
def viewProfile(request, id):
    user = User.objects.get (email=id)
    favAuthors = user.favoriteAuthors.distinct ( )
    favGenres = user.favoriteGenres.filter ( )

    # display the user's book that
    books = Book.objects.filter (owner_id=user.id, available=True, shared=False)

    # determine whether we are currently following the user or not based off of the user's following list and check if email exists. Pass in boolean value to template.

    this_user = User.objects.get (pk=request.user.id)

    if user in this_user.follow_list.all ( ):
        following = True
    else:
        following = False

    return render (request, 'profileCustomization/viewProfile.html',
                   {'user': user, 'favAuthors': favAuthors, 'favGenres': favGenres,
                    'books': books, 'following': following})

@login_required 
def viewMyProfile(request):
    return render(request, 'profileCustomization/viewProfile.html', {'user': request.user})


@login_required
def addBook(request):
    if request.method == "POST":
        addBook = addBookForm (request.POST)
        addAuthor = addAuthorForm (request.POST)
        addGenre = addGenreForm (request.POST)

        if addBook.is_valid ( ) and addAuthor.is_valid ( ) and addGenre.is_valid ( ):
            user = request.user
            book = addBook.save (commit=False)
            book.owner_id = request.user.id
            author = addAuthor.save (commit=False)
            genre = addGenre.save (commit=False)
            book.author = author
            book.genre = genre
            author.save ( )
            genre.save ( )
            book.save ( )

            if book.favorite is True:
                user.favoriteAuthors.add (author)
                user.favoriteGenres.add (genre)

            return redirect (reverse ('accounts:myBookShelf'))
    else:
        addBook = addBookForm ( )
        addAuthor = addAuthorForm ( )
        addGenre = addGenreForm ( )
    return render (request, "accounts/addBook.html", {'addBook': addBook, 'addAuthor': addAuthor, 'addGenre': addGenre})


@login_required
def user_logout(request):
    return HttpResponseRedirect (reversed ('your_app:login'))


@login_required
def edit_address(request):
    if request.method == "POST":
        form = EditAddress (request.POST or None, instance=request.user, use_required_attribute=False)
        if form.is_valid ( ):
            form.save ( )
            return render (request, 'profileCustomization/editProfile.html')

    else:
        form = EditAddress (request.POST or None, instance=request.user, use_required_attribute=False)
    return render (request, 'profileCustomization/editAddress.html', {'form': form})


@login_required ( )
def viewFavBooks(request):
    favBooks = Book.objects.filter (owner_id=request.user.id, favorite=True)

    return render (request, 'profileCustomization/myFavoriteBooks.html', {'favBooks': favBooks})


@login_required ( )
def viewFavAuthors(request):
    user = request.user
    favAuthors = user.favoriteAuthors.distinct ( )

    uniqueAuthors = []
    for fa in favAuthors:
        if fa not in uniqueAuthors:
            uniqueAuthors.append (fa)

    # now we will also get the favorite authors from the books that were marked as favorites again we will still want to keep it unique

    return render (request, 'profileCustomization/myFavoriteAuthors.html', {'uniqueAuthors': uniqueAuthors})


@login_required ( )
def viewFavGenres(request):
    user = request.user
    favGenres = user.favoriteGenres.filter ( )
    uniqueGenres = []
    for fg in favGenres:
        if fg.name not in uniqueGenres:
            uniqueGenres.append (fg.name)

    return render (request, 'profileCustomization/myFavoriteGenres.html', {'uniqueGenres': uniqueGenres})


@login_required ( )
def addFavAuthors(request):
    if request.method == "POST":
        favAuthor = addAuthorForm (request.POST)

        if favAuthor.is_valid ( ):
            author = favAuthor.save (commit=False)
            author.favorite = True
            author.save ( )
    else:
        favAuthor = addAuthorForm (request.POST)

    return render (request, 'profileCustomization/addFavAuthor.html', {'favAuthor': favAuthor})


@login_required ( )
def deleteBook(request, pk):
    # whenever we delete a book, we also want to go through and delete the related author as well as the related genre.
    book = get_object_or_404 (Book, pk=pk)
    author = book.author
    genre = book.genre
    book.delete ( )
    author.delete ( )
    genre.delete ( )
    return redirect ('accounts:myBookShelf')


@login_required ( )
def viewBook(reqeust, pk):
    # we may have several books in our library so the bookshelf page may not want to get overflowed with loads of book, so we want to keep
    # this page as clean as we can.
    book = get_object_or_404 (Book, pk=pk)

    return render (reqeust, 'Bookshelf/bookDetail.html', {'book': book})


@login_required ( )
def edit_book(request, pk):
    book = get_object_or_404 (Book, pk=pk)

    if request.method == "POST":
        form = EditBook (request.POST, instance=book)
        if form.is_valid ( ):
            book = form.save ( )

            book.save ( )
            return redirect ('accounts:myBookShelf')
    else:
        form = EditBook (instance=book)
    return render (request, 'Bookshelf/editBook.html', {'form': form})


@login_required ( )
def changeBookVisibility(request, pk):
    book = get_object_or_404 (Book, pk=pk)

    if not book.available:
        book.available = True
        book.save ( )

    elif book.available:
        book.available = False
        book.save ( )

    return redirect ('accounts:myBookShelf')


@login_required ( )
def findBook(request):
    # get all of the user objects, except for the currently logged in user.
    users = User.objects.exclude (pk=request.user.id)

    # get some of the favorite authors of the user (0 - 3) objects only.

    # get some of the favorite genres of the user (0 - 3) objects only.

    # get some of the favorite books of the user (0 - 3) objects only.

    # Compare the favorites of the users and determine whether we should suggest them to the currently logged in user. We will build a list of suggestions.

    return render (request, 'Social/findBook.html', {'users': users})


@login_required ( )
def follow(request, pk):
    user_to_add = User.objects.get (pk=pk)
    this_user = User.objects.get (pk=request.user.id)
    this_user.follow_list.add (user_to_add)

    # return a message indicating that user was added to following list.
    messages.success (request, 'User Added To My Followings List.')
    return HttpResponseRedirect ('/account/viewProfile/' + str (user_to_add.email))


@login_required ( )
def followList(request):
    user = User.objects.get (pk=request.user.id)
    this_user = User.objects.get (pk=request.user.id)
    list = this_user.follow_list.all ( )

    return render (request, 'Social/myFollowings.html', {'list': list})


@login_required ( )
def unfollow(request, pk):
    user_to_unfollow = User.objects.get (pk=pk)
    this_user = User.objects.get (pk=request.user.id)
    this_user.follow_list.remove (user_to_unfollow)
    # return a message indicating that user was removed from our followings list.
    messages.success (request, 'User Removed From My Followings List.')
    return HttpResponseRedirect ('/account/viewProfile/' + str (user_to_unfollow.email))


@login_required ( )
def requestABook(request, pk):
    user_to_request_from = User.objects.get (pk=pk)

    # display the list of available books that the user can share at the moment
    books = Book.objects.filter (owner_id=pk, available=True, shared=False)

    if request.method == 'POST':
        new_message = messageForm (request.POST)

        if new_message.is_valid ( ):
            message = new_message.save (commit=False)
            message.sender = request.user
            message.reciever = user_to_request_from
            message.save ( )
            return redirect ('accounts:customerView')


    else:
        message = messageForm ( )
    return render (request, 'Social/requestABook.html',
                   {'requestee': user_to_request_from, 'books': books, 'messageForm': messageForm})


@login_required ( )
def myMessages(request):
    # by default get all of the messages.
    # load all of your messages both sent and recieved
    recieved_messages = Message.objects.filter (reciever_id=request.user.id).order_by('-created_on')
    sent_messages = Message.objects.filter (sender_id=request.user.id).order_by('-created_on')
    messages = recieved_messages | sent_messages
    messages.order_by('-created_on')

    if (request.GET.get ('all_messages')):
        # load all of your messages both sent and recieved
        recieved_messages = Message.objects.filter (reciever_id=request.user.id).order_by('-created_on')
        sent_messages = Message.objects.filter (sender_id=request.user.id).order_by('-created_on')
        messages = recieved_messages | sent_messages
        messages.order_by('-created_on')

    elif (request.GET.get ('sent_messages')):
        messages = Message.objects.filter (sender_id=request.user.id).order_by('-created_on')

    elif (request.GET.get ('recieved_messages')):
        messages = Message.objects.filter (reciever_id=request.user.id).order_by('-created_on')
    return render (request, 'Social/myRequests.html', {'messages': messages})


@login_required ( )
def deleteMessages(request, pk):
    message = get_object_or_404 (Message, pk=pk)
    message.delete ( )
    return redirect ('accounts:myMessages')

@login_required ( )
def wishlist(request):
    return render (request, 'accounts/myWishlist.html', {'wishlist': wishlist})


@login_required()
def deletePost(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('accounts:customerView')