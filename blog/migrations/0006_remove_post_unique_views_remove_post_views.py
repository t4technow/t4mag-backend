# Generated by Django 4.2 on 2023-05-05 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_unique_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='unique_views',
        ),
        migrations.RemoveField(
            model_name='post',
            name='views',
        ),
    ]