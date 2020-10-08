from django.db.models.signals import post_save
from django.dispatch import receiver
from TagPost.models import TagPost
from blog.models import Post

import os

# this function is fired every time a new post is created.
# # Adds the tag.
# @receiver(post_save, sender=Post)
# def create_tag(sender, instance, created, **kwargs):
#     print("kwargs: ", kwargs['signal'])
#     if created:
#         selectedTags = TagPost.objects.filter(pk__in=request.POST.getlist('tags'))
#         #form.instance.tags.set(selectedTags)
#         #Profile.objects.create(user=instance)

# @receiver(post_save, sender=Post)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()


           