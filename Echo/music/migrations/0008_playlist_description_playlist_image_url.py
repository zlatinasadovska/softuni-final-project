# Generated by Django 5.1.3 on 2024-11-29 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_remove_album_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
