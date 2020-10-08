from django import forms
from TagPost.models import TagPost

class TagCreateForm(forms.ModelForm):

    tag = forms.CharField(max_length=25, widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Tag",}), label="Tag", required=True)
    description = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Description",}), label="Description", required=False)

    class Meta:
        model = TagPost
        fields = ['tag', 'description']
