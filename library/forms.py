from django import forms
from .models import Book, ShareBook
from bootstrap_modal_forms.forms import BSModalModelForm

class BookForm(BSModalModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'summary', 'available']

class ShareBookForm(forms.ModelForm):
    class Meta:
        model = ShareBook
        fields = ['books']
