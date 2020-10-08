from users.models import Profile
from django.utils import timezone
from django.db import models

class CommentPost(models.Model):
    authorComment = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment