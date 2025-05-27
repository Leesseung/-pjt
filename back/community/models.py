from django.conf import settings
from django.db import models

class Post(models.Model):
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title       = models.CharField(max_length=100)
    content     = models.TextField()
    image       = models.ImageField(upload_to="posts/%Y/%m/%d/", blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post        = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent      = models.ForeignKey("self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    content     = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)
