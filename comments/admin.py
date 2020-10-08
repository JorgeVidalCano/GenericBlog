from django.contrib import admin
from comments.models import CommentPost
from blog.models import Post
from users.models import Profile
# Register your models here.

@admin.register(CommentPost)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ["comment_date"]
    list_display= ("name", "comment", "post", "comment_date")
    search_fields= ["name", "post"]
    
    def name(self, obj):
        return str(Profile.objects.get(user=obj.authorComment.user)).replace("Profile", "")

    def post(self, obj):
        return Post.objects.get(comments=obj)