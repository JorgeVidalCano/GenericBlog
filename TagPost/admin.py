from django.contrib import admin
from TagPost.models import TagPost

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('tag', 'description')
    