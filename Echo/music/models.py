from django.db import models
from Echo.accounts.models import UserProfile


class Artist(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True,
    )
    spotify_id = models.CharField(
        max_length=50,
        unique=True,
        default="default_spotify_id",
    )

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(
        max_length=100,
    )
    artist = models.ForeignKey(
        to=Artist,
        related_name='albums',
        on_delete=models.CASCADE,
    )
    release_date = models.DateField(
        null=True,
        blank=True,
    )
    spotify_id = models.CharField(
        max_length=50,
        unique=True,
        default="default_spotify_id",
    )

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(
        max_length=100,
    )
    artist = models.ForeignKey(
        to=Artist,
        related_name='tracks',
        on_delete=models.CASCADE,
    )
    album = models.ForeignKey(
        to=Album,
        related_name='tracks',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    track_image = models.ImageField(
        upload_to='track_images/',
        blank=True,
        null=True,
    )
    track_file = models.FileField(
        upload_to='track_files/',
        blank=True,
        null=True,
    )
    preview_url = models.URLField(
        max_length=200,
        null=True,
        blank=True,
    )
    spotify_id = models.CharField(
        max_length=50,
        unique=True,
        default="default_spotify_id",
    )
    duration_ms = models.IntegerField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(
        max_length=100,
    )
    user = models.ForeignKey(
        to=UserProfile,
        related_name='playlists',
        on_delete=models.CASCADE,
    )
    tracks = models.ManyToManyField(
        to=Track,
        related_name='playlists',
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
