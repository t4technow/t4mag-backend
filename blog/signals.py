from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os

from users.models import User  # Import the User model from the other app
from .models import Post  # Import the Post model from this app

@receiver(post_save, sender=Post)
def resize_post_images(sender, instance, created, **kwargs):
    if created:
        image_field = instance.featured_image
        if image_field:
            # Resize and save the post image
            resize_image(image_field.path, image_field.path, (image_field.width, image_field.height), 'webp', 'featured')


def resize_image(image_path, output_path, size, format, subfolder=None):
    image = Image.open(image_path)
    image = image.resize(size, Image.ANTIALIAS)

    if subfolder:
        output_dir = os.path.dirname(image_path)
        output_dir = os.path.join(output_dir, subfolder)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, os.path.basename(output_path))

    image.save(output_path, format=format)
