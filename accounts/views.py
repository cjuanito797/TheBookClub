from django.shortcuts import render, get_object_or_404, redirect
from .models import User

from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from .forms import userRegistation, CustomUserCreationForm


# Create your views here.
def Signup(request):
    context = {}
    if request.POST:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('library:home')
        else: #GET request
            form = CustomUserCreationForm()
            context['registration_form'] = form
        return render(request, 'registration/register.html', context)
