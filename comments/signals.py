from django.db.models.signals import post_save
from django.dispatch import receiver
from comments.models import CommentPost
from blog.models import Post

# this function is fired every time a new user registers.
# Creates a profile for every new user.
@receiver(post_save, sender=CommentPost)
def create_profile(sender, instance, created, **kwargs):
    pass
        #Post.objects.get()
