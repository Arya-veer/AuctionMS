from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class Usersregistration(UserCreationForm):
    email=forms.EmailField(required=False)
    # DOB=forms.DateField(required=False)
    # First_name=forms.CharField(required=True)


    class Meta:
        model=User
        fields=['username','first_name','email','password1','password2','last_name']

