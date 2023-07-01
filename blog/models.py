from django.db import models
from users.models import User
from django.utils import timezone

from PIL import Image
import os
from django.conf import settings

class Tag(models.Model):
  title = models.CharField(max_length = 30)
  slug = models.SlugField(unique=True)

  class Meta:
    verbose_name = 'Tag'
    verbose_name_plural = 'Tags'

  def __str__(self):
    return self.title


class Category(models.Model):
  title = models.CharField(max_length=30)
  slug = models.SlugField(unique=True)
  accent = models.CharField(max_length=20, blank=True, default='#0073ff')

  class Meta:
    verbose_name = 'Category'
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.title

class Post(models.Model):

  class PostObjects(models.Manager):
    def get_queryset(self):
      return super().get_queryset().filter(status='published')

  
  VISIBILITY = (
    ('published', 'published'),
    ('draft', 'draft')
  )

  CONTENT_TYPE = (
    ('post', 'post'),
    ('page', 'page')
  )

  ALLOW_COMMENTS = (
    ('allow', 'allow'),
    ('no comments', 'no comments')
  )

  title = models.CharField(max_length=300)
  slug = models.SlugField(unique_for_date='created_at', blank=True)
  featured_image = models.ImageField(upload_to='post/original')
  body = models.TextField()
  excerpt = models.TextField(null=True, blank=True)
  author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
  category = models.ForeignKey(Category, related_name= 'post_category', on_delete=models.PROTECT, null=True, blank=True )
  tags = models.ManyToManyField(Tag, related_name='post_tags', blank=True)
  status = models.CharField(max_length=30, choices = VISIBILITY, default='published')
  content_type = models.CharField(max_length=30, choices=CONTENT_TYPE, default='post')
  allow_comments = models.CharField(max_length=30, choices=ALLOW_COMMENTS, default='allow')
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(auto_now=True)
  views = models.PositiveIntegerField(default=0)
  
  objects = models.Manager()
  postobjects = PostObjects()
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Post'
    verbose_name_plural = 'Posts'

  def __str__(self):
      return self.title
    
  # @property
  # def thumbnail_sm_url(self):
  #     return self._generate_image_url('thumbnails', 'thumbnail-sm')

  # @property
  # def thumbnail_url(self):
  #     return self._generate_image_url('thumbnails', 'thumbnail')

  # @property
  # def featured_image_url(self):
  #     return self._generate_image_url('featured', 'featured')

  # def _generate_image_url(self, folder, size):
  #   original_image_path = str(self.featured_image.url)
  #   image_filename = original_image_path.split('/')[-1]  # Extract the image filename
  #   print(image_filename, '---------------------image_filename----------------------------')
  #   image_filename_without_extension = image_filename.split('.')[0]  # Remove the file extension
  #   image_filename_with_size = f"{image_filename_without_extension}_{size}.webp"  # Append the size to the filename
  #   image_temp_url = original_image_path.replace('original/', f'{folder}/')  # Generate the full image URL
  #   image_url = image_temp_url.replace(image_filename, image_filename_with_size)  # Generate the full image URL

  #   # Replace the media URL in the image URL
  #   media_root = str(settings.MEDIA_ROOT)
  #   media_url = str(settings.MEDIA_URL)
  #   image_url = image_url.replace(media_root, media_url)
    
  #   domain = settings.SITE_DOMAIN
  #   image_url = f"http://{domain}{image_url}"

  #   return image_url

  # def save(self, *args, **kwargs):
  #     super().save(*args, **kwargs)
  #     if self.featured_image:
  #         image = Image.open(self.featured_image)
  #         sizes = [(100, 100), (306, 209)]
  #         resized_images = resize_image(image, sizes)
  #         for img_io, filename in resized_images:
  #             img = Image.open(img_io)
  #             img.convert('RGB')  # Convert the image to RGB format
  #             img.save(self.featured_image.path.replace('original/', 'thumbnails/') + filename)
  #             img_io.close()

  #         # Save the original image as webp format in the 'featured' folder
  #         original_image = Image.open(self.featured_image.path)
  #         original_image.convert('RGB')  # Convert the image to RGB format
  #         original_image.save(self.featured_image.path.replace('original/', 'featured/').replace('.jpg', '.webp'), format='webp')


  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    if self.featured_image:
        image = Image.open(self.featured_image)
        sizes = [(100, 100, 'thumbnail-sm'), (306, 209, 'thumbnail')]
        for width, height, size_name in sizes:
            resized_image = image.resize((width, height), Image.ANTIALIAS)
            folder = f'post/{size_name}'
            os.makedirs(os.path.join(settings.MEDIA_ROOT, folder), exist_ok=True)
            filename = self.featured_image.name.split('/')[-1]
            extension = self.featured_image.name.split('.')[-1]
            renamed = filename.replace(extension, 'webp')
            image_path = f'{folder}/{renamed}'
            resized_image.save(settings.MEDIA_ROOT / image_path, format='webp')

        original_image = Image.open(self.featured_image.path)
        original_image.convert('RGB')  # Convert the image to RGB format
        directory = str(settings.MEDIA_ROOT) + '/post/'
        os.makedirs(os.path.join(directory, 'featured'), exist_ok=True)

        # Extract the file extension dynamically
        file_extension = os.path.splitext(self.featured_image.path)[1]
        # Replace the file extension with '.webp' for the new image path
        new_image_path = self.featured_image.path.replace('original/', 'featured/').replace(file_extension, '.webp')

        original_image.save(new_image_path, format='webp')
  
  @property
  def thumbnail_sm_url(self):
      return self._generate_image_url('thumbnail-sm', 'thumbnail-sm')

  @property
  def thumbnail_url(self):
      return self._generate_image_url('thumbnail', 'thumbnail')

  @property
  def featured_image_url(self):
      return self._generate_image_url('featured', 'featured')

  def _generate_image_url(self, folder, size):
      original_image_path = str(self.featured_image.url)
      image_filename = original_image_path.split('/')[-1]  # Extract the image filename
      image_filename_without_extension = image_filename.split('.')[0]  # Remove the file extension
      image_filename_with_size = f"{image_filename_without_extension}_{size}.webp"  # Append the size to the filename
      image_temp_url = f"{original_image_path.replace('original/', f'{folder}/')}.webp"  # Generate the full image URL
      image_url = image_temp_url.replace(image_filename, image_filename_without_extension)  # Generate the full image URL

      # Replace the media URL in the image URL
      media_root = str(settings.MEDIA_ROOT)
      media_url = str(settings.MEDIA_URL)
      image_url = image_url.replace(media_root, media_url)

      domain = settings.SITE_DOMAIN
      image_url = f"https://{domain}{image_url}"

      return image_url

class Comment(models.Model):

  post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  body = models.TextField()
  parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    verbose_name = 'Comment'
    verbose_name_plural = 'Comments'

  def __str__(self):
      return self.body
