from django import forms
from .models import Profile
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Username",}), label="Username")
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class':'form-control', "placeholder":"Email",}), label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control',"placeholder": "Password", }), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'form-control',"placeholder": "Repeat password",}), label="Repeat password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"First name",}), label="First name", required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Last name",}), label="Last name", required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs = {'class':'form-control', "placeholder":"Email",}), label="Email", required=False)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    shortDescription = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Short description",}), label="Short description", required=False)
    aboutMe = forms.CharField(widget=forms.Textarea(attrs = {'class':'form-control', "placeholder":"About me",}), label="", required=False)
    telephone = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Telephone",}), label="Telephone", required=False)
    profileImage = forms.ImageField(widget=forms.FileInput(), label="Profile Image", required=False)

    class Meta:
        model = Profile
        fields = ['shortDescription', 'telephone', 'aboutMe', 'profileImage']

class UserUpdateEmailForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']