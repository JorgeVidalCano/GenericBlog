from django.db import models
from django.utils.html import mark_safe

class ConfigBlog(models.Model):
    blogTitle = models.CharField(max_length=15)
    footerTitle = models.CharField(max_length=50)
    logo = models.ImageField(upload_to ='postImages', blank=True)
    abouts = models.ManyToManyField("ConfigBlog.AboutFields")

    def __str__(self):
        return "Blog info"

    @property
    def thumbnail_preview_list(self):    
        if self.logo:
            return mark_safe('<img src="{}" width="100px" height="100px" class="img-thumbnail" />'.format(self.logo.url))
        return ""

class AboutFields(models.Model):

    title = models.CharField(max_length= 15)
    content = models.CharField(max_length= 100)
    icon = models.CharField(max_length= 30, blank=True)
    conf = models.ForeignKey("ConfigBlog.ConfigBlog", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title