# Generated by Django 5.1.3 on 2024-11-29 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0009_remove_track_track_file_alter_track_spotify_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='spotify_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
