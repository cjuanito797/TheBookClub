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


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', )


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)

class userRegistation(forms.ModelForm):
    first_name = forms.CharField (label='', required=True, widget=forms.TextInput (attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField (label='', required=True, widget=forms.TextInput (attrs={'placeholder': 'Last Name'}))
    # email = forms.CharField(label='', widget=forms.EmailInput(attrs={'placeholder', 'johndoe@example.com'}))
    email = forms.CharField (label='', max_length=100,
                             widget=forms.EmailInput
                             (attrs={'placeholder': 'Enter your email'}))
    password = forms.CharField (label='', widget=forms.PasswordInput (attrs={'placeholder': 'Password'}), required=True)
    password2 = forms.CharField (label='',
                                 widget=forms.PasswordInput (attrs={'placeholder': 'Verify Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError ('Passwords don\'t match.')
        return cd['password2']
