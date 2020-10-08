from django import forms
from .models import CommentPost


class NewCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control'}), label="")
   
    class Meta:
        model = CommentPost
        fields = ['comment']