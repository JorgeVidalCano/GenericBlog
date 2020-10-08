from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db import models

class TagPost(models.Model):
    tag = models.CharField(max_length=25, unique=True) 
    slug = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.tag)
        super(TagPost, self).save(*args, **kwargs)

    
    def allTags(self):
        return TagPost.objects.all()
