from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('shortcode', 'get_display_url', 'published', 'likes_count', 'comments_count', 'caption', 'query',
                    'is_video', 'video_view_count')
    readonly_fields = ['id', 'owner_id', 'shortcode', 'is_video', 'query']

    list_filter = ('is_video', 'query')

    def get_display_url(self, obj):
        if obj.display_url:
            return mark_safe(f'<a href="{obj.display_url}" target="_blank">{obj.display_url[:20]}...</a>')
        else:
            return '-'


admin.site.register(Post, PostAdmin)
