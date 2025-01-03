# Generated by Django 5.1.3 on 2024-12-11 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0018_album_cover_image_artist_genres_artist_spotify_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='music.artist'),
        ),
    ]
