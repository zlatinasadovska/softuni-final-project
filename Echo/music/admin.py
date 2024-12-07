from django.contrib import admin
from Echo.music.models import Artist, Album, Track, Playlist


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date')
    list_filter = ('artist', 'release_date')
    search_fields = ('title', 'artist__name')
    ordering = ('release_date', 'title')


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album')
    list_filter = ('artist', 'album')
    search_fields = ('title', 'artist__name', 'album__title')
    ordering = ('album', 'title')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user',)
    search_fields = ('name', 'user__email')
    ordering = ('created_at',)
