
from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_auths.models import User

class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        