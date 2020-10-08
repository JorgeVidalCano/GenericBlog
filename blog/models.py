from comments.models import CommentPost
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.utils.html import mark_safe

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = RichTextUploadingField()
    meta = models.CharField(max_length=155, blank=True)
    date_posted = models.DateTimeField(default="9999-01-01")
    date_created = models.DateField(default=timezone.now)
    publish = models.BooleanField(default=False)
    PostImages = models.ImageField(upload_to ='postImages', blank=True, default='defaultBlog.jpg')
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(CommentPost, related_name='commentPost', blank=True)
    tags = models.ManyToManyField("TagPost.TagPost", related_name='TagPost', blank=True)

    def save(self, *args, **kwargs):
        if self.publish == True:
            self.date_posted = timezone.now()
        super(Post, self).save(*args, **kwargs)

    def publicate(self):
        now = timezone.now()
        if now > self.date_posted:
            self.publish = True
            self.save()
        return
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug':self.slug})

    def countLikes(obj):
        return LikeCounter.objects.filter(post= obj).filter(value="like").count()

    def countUnlikes(obj):
        return LikeCounter.objects.filter(post= obj).filter(value="unlike").count()

    def countComments(obj):
        return Post.objects.get(title= obj.title).comments.count()
    
    def findTags(obj):
        return Post.objects.get(title= obj.title).tags.all()
    
    @property
    def thumbnail_preview_post(self):    
        if self.PostImages:
            return mark_safe('<img src="{}" width="740" height="100%" class="img-thumbnail" />'.format(self.PostImages.url))
        return ""
    
    @property
    def thumbnail_preview_list(self):    
        if self.PostImages:
            return mark_safe('<img src="{}" width="40px" height="30px" class="img-thumbnail" />'.format(self.PostImages.url))
        return ""
        
class LikeCounter(models.Model):
    class Meta:
        unique_together = ['user', 'post']

    likeOptions = (
        ("like", "Like"),
        ("unlike", "Unlike")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=likeOptions, blank=True, max_length=10)

    def __str__(self):
        return f'{self.user.username}: {self.post.title}'

    def addLike(self, post, user, value):
        ## checks if the user has a like in the post, if not it creates one else updates it.
        checkLike = LikeCounter.objects.filter(post= post, user= user)
        if checkLike.count() == 0:
            l = LikeCounter.objects.create(post= post, user= user, value= value)
        else:
            LikeCounter.objects.filter(post= post, user= user).update(value= value)