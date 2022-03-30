from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet, inlineformset_factory
from django.forms import modelformset_factory
from .models import User
from django.core.exceptions import ValidationError
from django.forms import HiddenInput
from django.forms.models import ModelForm
from .models import User
from library.models import Book, Author, Genre


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'street_num', 'city', 'state', 'zipcode',)

    def __init__(self, *args, **kwargs):
        super (RegistrationForm, self).__init__ (*args, **kwargs)

        for fieldname in ['password1','password2',]:

            self.fields[fieldname].help_text = None

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EditAddress(forms.ModelForm):
    class Meta:
        model = User

        fields = ("street_num", "city", "state", "zipcode")

class addBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "summary", "price", "isbn", "favorite")

class addAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("first_name", "last_name")

class addGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ("name", )