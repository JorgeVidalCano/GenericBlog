from django.contrib.auth.models import Group
from django.contrib import admin
from blog.models import Post, LikeCounter

admin.site.unregister(Group)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    readonly_fields =["date_created", 'thumbnail_preview_post']
    list_display = ('title', 'Likes', 'Unlikes', 'Comments', 'date_posted', 'date_created', 'publish', 'thumbnail_preview_list')
    ordering = ('-date_created', 'publish')

    search_fields = ('title', 'countComments', 'date_created', 'publish')

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

    # Count likes
    def Likes(self, obj):
        return Post.countLikes(obj)
    # Count dislikes
    def Unlikes(self, obj):
        return Post.countUnlikes(obj)
    # Count comments
    def Comments(self, obj):
        return Post.objects.get(title=obj.title).comments.count()


@admin.register(LikeCounter)
class liAdmin(admin.ModelAdmin):
    pass

