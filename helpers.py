from PIL import Image
from io import BytesIO
import os


def resize_image(image, sizes, format='webp'):
    resized_images = []
    for size in sizes:
        resized_img = image.copy()
        resized_img.thumbnail(size)
        output_io = BytesIO()
        resized_img.save(output_io, format=format)
        output_io.seek(0)
        resized_images.append((output_io, f'{size[0]}x{size[1]}.{format}'))
    return resized_images
