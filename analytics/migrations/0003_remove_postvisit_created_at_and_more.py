# Generated by Django 4.2 on 2023-05-05 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0004_post_views'),
        ('analytics', '0002_rename_postview_postvisit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postvisit',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='postvisit',
            name='user_agent',
        ),
        migrations.AddField(
            model_name='postvisit',
            name='browser_family',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='postvisit',
            name='last_visit',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='postvisit',
            name='os_family',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='postvisit',
            name='unique_views',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='postvisit',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='postvisit',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='postvisit',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
    ]
