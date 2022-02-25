from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from .models import User
from django.contrib.auth import login, authenticate
from django.urls import reverse
from django.views.generic import FormView, TemplateView
from .forms import RegistrationForm


# Create your views here.
class registration_view(FormView):
    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('library:home'))
        return render(request, 'registration/register.html', {'form' : form})

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form' : form})
