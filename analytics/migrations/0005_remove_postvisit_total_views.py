# Generated by Django 4.2 on 2023-05-05 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_visitor_postvisit_total_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postvisit',
            name='total_views',
        ),
    ]
