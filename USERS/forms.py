from django import forms
from .models import Profile

class EditUserForm(forms.Form):
    username = forms.CharField(label='UserName', required=True,max_length=20)
    email = forms.EmailField(label='Email', required=True)
    role = forms.ChoiceField(choices=(('Staff', 'Staff'), ('Faculty', 'Faculty'), ('Student', 'Student')), label='Role', required=True)
