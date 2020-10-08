from django.contrib.auth.models import User
from django.db import models
from PIL import Image
import os

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=50, blank=True)
    shortDescription = models.TextField(max_length=50, default="Add a short description about you.")
    aboutMe = models.CharField(max_length=500, default="Write something about you.")
    profileImage = models.ImageField(upload_to ='profileImages', blank=True, default='profileImages/default.jpg')

    favoritePosts = models.ManyToManyField("blog.Post", related_name='favoritePosts', blank=True)

    def __str__(self):
        return f'{self.user.username.title()} Profile'

    def isFavorite(self, post, user):
        p = Profile.objects.get(user=user)
        f = p.favoritePosts.filter(title=post.title)
                
        if f:
            return True
        return False

    def addRemoveFav(self, user, post, isFavorite):
        user_profile = Profile.objects.get(user=user)
        
        if str(isFavorite) == "True": 
            user_profile.favoritePosts.remove(post)
        else:
            user_profile.favoritePosts.add(post)
        return

    # def save(self, *args, **kwargs):
    #     oldProfileImg = Profile.objects.get(user=self.user).profileImage.path # stores the previous profile img to delete it
    #     super().save(*args, **kwargs)
    #     common_sizePX = 300
    #     img = Image.open(self.profileImage.path)
    #     if img.height > common_sizePX or img.width > common_sizePX:
    #         output_size = (common_sizePX, common_sizePX)
    #         img.thumbnail(output_size)
    #         img.save(self.profileImage.path)

    #         try:
    #             if os.path.exists(oldProfileImg):
    #                 os.remove(oldProfileImg)
    #         except Exception as ex:
    #             print(ex)
