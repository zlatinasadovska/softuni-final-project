# Generated by Django 5.1.3 on 2024-12-11 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0019_alter_album_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='spotify_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
