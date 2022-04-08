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
from .models import User, Message
from library.models import Book, Author, Genre


class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name', 'street_num', 'city', 'state', 'zipcode',)

    def __init__(self, *args, **kwargs):
        super (RegistrationForm, self).__init__ (*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['placeholder'] = visible.field.label

        for fieldname in ['password1','password2',]:
            self.fields[fieldname].help_text = None

class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class EditAddress(forms.ModelForm):
    class Meta:
        model = User

        fields = ("street_num", "city", "state", "zipcode")

class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "bio", "street_num", "city", "state", "zipcode")

    def __init__(self, *args, **kwargs):
            super (EditProfile, self).__init__ (*args, **kwargs)

            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
                visible.field.widget.attrs['placeholder'] = visible.field.label        


class EditBook(forms.ModelForm):
    class Meta:
        model = Book

        fields = ("title", "summary", "price", "available", "shared")


class addBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "summary", "price", "isbn", "favorite")

    def __init__(self, *args, **kwargs):
            super (addBookForm, self).__init__ (*args, **kwargs)

            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
                if visible.name == 'favorite':
                    visible.field.widget.attrs['class'] = 'form-check-input border-white ml-1'

class addAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ("first_name", "last_name")


    def __init__(self, *args, **kwargs):
            super (addAuthorForm, self).__init__ (*args, **kwargs)

            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

class addGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ("name", )


    def __init__(self, *args, **kwargs):
            super (addGenreForm, self).__init__ (*args, **kwargs)

            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

class messageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("message", )