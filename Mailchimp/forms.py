from django import forms
from .models import Signup


class EmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "name": "email",
        "id": "email",
        "placeholder": "Type your email address",
        "class":"form-control"
    }), label="")

    class Meta:
        model = Signup
        fields = ('email', )