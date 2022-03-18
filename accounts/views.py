from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from library.models import Book


# Create your views here.
class registration_view(FormView):
    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:user_login'))
        return render(request, 'registration/register.html', {'form' : form})

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form' : form})

def user_login(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(request,
                            username=cd['username'],
                            password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(redirect('accounts:customerView'))
            else:
                return HttpResponse('Disabled Account')
        else:
            return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form' : form})

@login_required
def customerView(request):

    return render(request, 'accounts/base.html')

@login_required
def myBookShelf(request):
    myBooks = Book.objects.filter(owner_id=request.user)
    return render(request, 'accounts/myBookshelf.html', {'myBooks' : myBooks})

@login_required
def editProfile(request):
    return render(request, 'profileCustomization/editProfile.html')

@login_required
def addBook(request):
    return render(request, 'accounts/addBook.html')

@login_required
def user_logout(request):
    return HttpResponseRedirect(reversed('your_app:login'))
