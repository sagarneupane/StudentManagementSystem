from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegisterUser(UserCreationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Enter Your Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Confirm Your Password")
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Enter Your Password")
    

class UserEditForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ['first_name',"last_name","email"]
        
        widgets = {
            "first_name":forms.TextInput(attrs={"class":"custominput","placeholder":"Your Firstname Here"}),
            "last_name":forms.TextInput(attrs={"class":"custominput","placeholder":"Your Last Name Here"}),
            "email":forms.TextInput(attrs={"class":"custominput","placeholder":"Your Email Here"}),
        }
        
    