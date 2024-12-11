from django.conf import settings
from django.db import models
from Echo.accounts.models import UserProfile


class Artist(models.Model):
    spotify_id = models.CharField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=255,
    )
    profile_picture = models.URLField(
        null=True,
        blank=True,
    )
    genres = models.TextField(
        null=True,
        blank=True,
    )
    spotify_url = models.URLField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name


class Album(models.Model):
    spotify_id = models.CharField(
        max_length=255,
        unique=True,
    )
    title = models.CharField(
        max_length=255,
    )
    artist = models.ForeignKey(
        Artist,
        related_name="albums",
        on_delete=models.CASCADE,
    )
    release_date = models.DateField(
        null=True,
        blank=True,
    )
    cover_image = models.URLField(
        null=True,
        blank=True,
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
        blank=True,
        null=True,
    )
    track_file = models.FileField(
        blank=True,
        null=True,
    )
    preview_url = models.URLField(
        null=True,
        blank=True,
    )
    spotify_id = models.CharField(
        max_length=50,
        unique=True,
        default="default_spotify_id",
    )
    spotify_url = models.URLField(
        null=True,
        blank=True,
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


class Testimonial(models.Model):
    text = models.TextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.text[:20]}"
