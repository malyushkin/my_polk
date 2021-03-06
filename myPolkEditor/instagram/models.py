from django.db import models
from django.contrib.postgres.fields import ArrayField
from datetime import datetime


class Post(models.Model):
    '''
    Основная модель – для хранения постов Instagram.
    '''
    id = models.BigIntegerField(primary_key=True)
    owner_id = models.BigIntegerField(null=False)
    shortcode = models.CharField(max_length=255, unique=True, null=False)
    post_url = models.CharField(max_length=255, null=False)
    display_url = models.CharField(max_length=500, null=False)
    published = models.DateTimeField(null=False)
    caption = models.TextField(null=True)
    likes_count = models.IntegerField(null=False)
    comments_count = models.IntegerField(null=False)
    comments = ArrayField(models.TextField(), blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_video = models.BooleanField(null=True, default=False)
    video_view_count = models.IntegerField(null=True)
    inst_caption = models.TextField(blank=True, null=True)
    query = models.CharField(max_length=255, null=False)
    tags = ArrayField(models.CharField(max_length=255), blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    status = models.BooleanField(null=False, default=True)
    # created_at = models.DateTimeField(auto_now_add=True, null=False)
    # updated_at = models.DateTimeField(auto_now_add=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Hashtag(models.Model):
    '''
    Хештег
    '''
    id = models.BigAutoField(primary_key=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    post_id = models.ForeignKey(Post, db_column='post_id', on_delete=models.CASCADE, null=True)


class NameEntity(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    generalized_name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)


class PostNameEntity(models.Model):
    post_id = models.ForeignKey(Post, db_column='post_id', on_delete=models.CASCADE, null=True)
    name_entity_id = models.ForeignKey(NameEntity, db_column='name_entity_id', on_delete=models.CASCADE, null=True)
