# Generated by Django 5.1.3 on 2024-11-27 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_remove_playlist_cover'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='updated_at',
        ),
    ]