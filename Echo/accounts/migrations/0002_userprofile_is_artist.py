# Generated by Django 5.1.3 on 2024-11-10 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_artist',
            field=models.BooleanField(default=False),
        ),
    ]