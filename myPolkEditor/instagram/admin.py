from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('shortcode', 'get_post_url', 'published', 'likes_count', 'comments_count', 'caption', 'query',
                    'is_video', 'video_view_count')
    readonly_fields = ['id', 'owner_id', 'shortcode', 'is_video', 'query']
    search_fields = ('caption', 'query')

    list_filter = ('is_video', 'query')

    def get_post_url(self, obj):
        if obj.display_url:
            return mark_safe(f'<a href="{obj.post_url}" target="_blank">{obj.post_url[:18]}...</a>')
        else:
            return '-'

    def get_queryset(self, request):
        queryset = super(PostAdmin, self).get_queryset(request)
        return queryset.filter(status=True)


admin.site.register(Post, PostAdmin)
