from django.db import models

class SocialMedia(models.Model):
    name = models.CharField(max_length= 35, unique= True)
    url = models.URLField(max_length= 150)
    logo = models.ImageField(upload_to= 'SocialMediaLogo')
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.name
