from django import forms
from .models import Book
from bootstrap_modal_forms.forms import BSModalModelForm

class BookForm(BSModalModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'price', 'summary', 'available']