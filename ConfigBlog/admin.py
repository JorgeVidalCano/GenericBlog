from ConfigBlog.models import ConfigBlog, AboutFields
from django.contrib import admin

class InlineAbout(admin.TabularInline):
    model = AboutFields
    extra = 1
    max_num = 8

@admin.register(ConfigBlog)
class ConfigAdmin(admin.ModelAdmin):
    inlines = [InlineAbout]
    list_display = ('blogTitle', 'thumbnail_preview_list')
    fieldsets =(
        (None, {
            "fields": (
                "blogTitle", "footerTitle", "logo"
            )
        }),
    )
    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    def has_add_permission(self, request, obj=None):
        # There can only be one register
        if ConfigBlog.objects.all().count() == 1:
            return False
        else:
            return True

    thumbnail_preview.short_description = 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True


     