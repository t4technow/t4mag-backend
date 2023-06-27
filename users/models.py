from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager

from PIL import Image
from helpers import resize_image

# Create your models here.

class User(AbstractUser):
  class AuthorObjects(models.Manager):
    def get_queryset(self):
      return super().get_queryset().filter(is_author=True)

  profile_pic = models.ImageField(upload_to='user/original')
  following_authors = models.ManyToManyField("self", symmetrical=False, related_name='followers', blank=True)
  is_author = models.BooleanField(default=False)
  bio = models.TextField(blank=True)
  
  objects = UserManager()
  authors = AuthorObjects()
  
  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'
      
  def __str__(self):
    return self.username

  def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_pic:
            image = Image.open(self.profile_pic)
            resized_images = resize_image(image, [(100, 100)])
            for img_io, filename in resized_images:
                img = Image.open(img_io)
                img.save(self.profile_pic.path.replace("original", filename), format='webp')
                img.close()
                img_io.close()
