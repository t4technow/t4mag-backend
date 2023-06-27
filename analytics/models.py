from django.db import models
from django.conf import settings
from django.utils import timezone
from blog.models import Post

class PostVisit(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    unique_views = models.PositiveIntegerField(default=0)
    browser_family = models.CharField(max_length=100, blank=True)
    os_family = models.CharField(max_length=100, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    last_visit = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.post.title
    
class Visitor(models.Model):
    ip_address = models.CharField(max_length=50)
    browser_family = models.CharField(max_length=50)
    os_family = models.CharField(max_length=50)