from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    role = forms.ChoiceField(choices=(('Staff', 'Staff'), ('Faculty', 'Faculty'), ('Student', 'Student')), label='Role', required=True)


class SigninForm(AuthenticationForm):
    username = forms.CharField(label='Enter Username or Library ID')

    class Meta:
        model = User
        fields = '__all__'



class EditProForm(forms.Form):
    username = forms.CharField(label='Username', required=True, max_length=20)
    email = forms.EmailField(label='Email', required=True)
    role = forms.ChoiceField(choices=(('Staff', 'Staff'), ('Faculty', 'Faculty'), ('Student', 'Student')), label='Role', required=True)