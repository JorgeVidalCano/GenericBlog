from django.contrib import admin
from SocialMedia.models import SocialMedia

@admin.register(SocialMedia)
class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "publish")
