from django.db.models.signals import pre_save
from .models import User
from django.dispatch import receiver

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from PIL import Image
# import os


# @receiver(post_save, sender=User)
# def resize_profile_picture(sender, instance, created, **kwargs):
#     if created:
#         image_field = instance.profile_pic
#         if image_field:
#             # Resize and save the profile picture
#             resize_image(image_field.path, image_field.path, (100, 100), 'webp')


# def resize_image(image_path, output_path, size, format):
#     image = Image.open(image_path)
#     image = image.resize(size, Image.ANTIALIAS)

#     image.save(output_path, format=format)



@receiver(pre_save, sender=User)
def update_user_fields(sender, instance, **kwargs):
    if instance.is_superuser:
        # Update the necessary fields for admin users
        instance.is_author = True
        instance.bio = "Admin User"