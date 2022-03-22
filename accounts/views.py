from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm, LoginForm, EditAddress
from django.contrib.auth.decorators import login_required
from library.models import Book


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
                             username=cd['username'],
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
    return render (request, 'accounts/base.html')


@login_required
def myBookShelf(request):
    myBooks = Book.objects.filter (owner_id=request.user)
    return render (request, 'accounts/myBookshelf.html', {'myBooks': myBooks})

@login_required
def editProfile(request):
    return render (request, 'profileCustomization/editProfile.html')

@login_required
def viewProfile(request, id):
    user = User.objects.get(user_id=id)
    favBooks = ['Book1', 'Book2', 'Book3']
    favAuthors = ['Author1', 'Author2', 'Author3']
    favGenres = ['Genre1', 'Genre2', 'Genre3']
    return render (request, 'profileCustomization/viewProfile.html', {'user': user, 'favBooks': favBooks, 'favAuthors': favAuthors, 'favGenres': favGenres})

@login_required
def addBook(request):
    return render (request, 'accounts/addBook.html')


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
