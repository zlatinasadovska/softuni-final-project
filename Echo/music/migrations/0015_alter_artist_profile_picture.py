# Generated by Django 5.1.3 on 2024-12-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0014_track_preview_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
