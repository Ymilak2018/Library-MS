from django import forms
from .models import Subject, Author, BookDetail

class BookForm(forms.ModelForm):
    class Meta:
        model = BookDetail
        fields = '__all__'


class SubForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'


class AuthForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'

