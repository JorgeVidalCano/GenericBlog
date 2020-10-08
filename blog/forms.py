from ckeditor.widgets import CKEditorWidget
from django.forms import SelectDateWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from blog.models import Post
from TagPost.models import TagPost

class PostCreateForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Title",}), label="Title", required=True)
    meta = forms.CharField(widget=forms.TextInput(attrs = {'class':'form-control', "placeholder":"Meta",}), label="Meta", required=True)
    content = forms.CharField(widget=CKEditorUploadingWidget(), label="")
    publish = forms.BooleanField(widget=forms.CheckboxInput(attrs = {'class':'form-check'}), label="Publish", required=False)
    postImage = forms.ImageField(label="", required=False)
    slug = forms.SlugField(widget=forms.TextInput(attrs = {'class':'form-control', 'readonly':'readonly'}), label="Url")
    tags = forms.ModelMultipleChoiceField(widget= forms.CheckboxSelectMultiple(attrs = {'class':'checkbox-tag'}), queryset=TagPost.objects.all(), label="", required=False)
    programPublication = forms.DateField(widget=SelectDateWidget(empty_label="Nothing", attrs={'class':'form-date'}), label="", required=True)

    class Meta:
        model = Post
        fields = ['title', 'meta', 'content', 'publish', 'postImage', 'slug', 'programPublication']

class PostPublishForm(forms.ModelForm):    
    publish = forms.BooleanField(widget=forms.CheckboxInput(attrs = {'class':'form-check'}), label="Publish", required=False)    
    class Meta:
        model = Post
        fields = ['publish']