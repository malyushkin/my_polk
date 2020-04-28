from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime


class Post(models.Model):
    '''
    Основная модель – для хранения постов Instagram.
    '''
    id = models.BigAutoField(primary_key=True)
    owner_id = models.BigIntegerField(null=False)
    shortcode = models.CharField(max_length=255, unique=True, null=False)
    display_url = models.CharField(max_length=255, null=False)
    published = models.DateTimeField(null=False)
    caption = models.TextField(null=True)
    likes_count = models.IntegerField(null=False)
    comments_count = models.IntegerField(null=False)
    comments = ArrayField(models.TextField(), blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_video = models.BooleanField(null=True, default=False)
    inst_caption = models.TextField(blank=True, null=True)
    query = models.CharField(max_length=255, null=False)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
