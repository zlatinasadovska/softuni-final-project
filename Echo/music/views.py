from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from Echo.music.forms import PlaylistForm
from Echo.music.models import Artist, Album, Track, Playlist
from Echo.spotify.spotify_helpers import import_track, import_album, search_spotify, import_artist


class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'music/artist_details.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.get_object()

        # Fetch detailed data for the artist from Spotify and save it
        spotify_artist = import_artist(artist.spotify_id)

        if spotify_artist:
            context['spotify_artist'] = spotify_artist
            context['albums'] = spotify_artist.albums.all()
            context['tracks'] = spotify_artist.tracks.all()  # Ensure tracks have preview_url

        return context


class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_details.html'
    context_object_name = 'album'

    def get_object(self):
        # Retrieve the album using the passed spotify_id
        spotify_id = self.kwargs.get('spotify_id')
        album = get_object_or_404(Album, spotify_id=spotify_id)
        return album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.get_object()

        # Fetch Spotify tracks for the album
        tracks = album.tracks.all()

        # Add tracks to the context
        context['tracks'] = tracks
        return context


class TrackDetailView(DetailView):
    model = Track
    template_name = 'music/track_details.html'
    context_object_name = 'spotify_track'

    def get_object(self, queryset=None):
        """Retrieve the track based on the spotify_id from the URL."""
        spotify_id = self.kwargs.get('spotify_id')
        track = Track.objects.filter(spotify_id=spotify_id).first()

        if not track:
            # If track doesn't exist in the database, fetch it from Spotify
            track = import_track(spotify_id)
            if not track:
                raise Http404("Track not found or unable to fetch from Spotify.")

        return track

    def get_context_data(self, **kwargs):
        """Add additional context for the template."""
        context = super().get_context_data(**kwargs)
        track = self.get_object()

        # Calculate the duration in minutes and seconds and add it to the context
        if track.duration_ms:
            duration_minutes = track.duration_ms // 60000
            duration_seconds = (track.duration_ms % 60000) // 1000
            context['duration'] = f"{duration_minutes}:{duration_seconds:02d}"
        else:
            context['duration'] = "Unknown duration"

        # Add the preview_url for the track to the context (if available)
        context['preview_url'] = track.preview_url

        return context


class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'music/playlist_details.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()

        # Get the sorting order from the GET parameter
        sort_order = self.request.GET.get('sort', 'default')

        # Sort the tracks based on the sorting order
        tracks = playlist.tracks.all()
        if sort_order == 'alphabetical':
            tracks = tracks.order_by('title')
        elif sort_order == 'reverse_alphabetical':
            tracks = tracks.order_by('-title')

        # Add data to the context
        context['tracks'] = tracks
        context['sort_order'] = sort_order
        return context


class CreatePlaylistView(LoginRequiredMixin, CreateView):
    model = Playlist
    form_class = PlaylistForm
    template_name = 'music/create_playlist.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, f'Playlist "{form.instance.name}" created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('playlist_detail', kwargs={'pk': self.object.pk})


@login_required
def delete_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    playlist.delete()
    messages.success(request, "Playlist deleted successfully!")
    return redirect('profile')


def remove_track_from_playlist(request, playlist_id, track_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to perform this action.")

    playlist = get_object_or_404(Playlist, pk=playlist_id)
    track = get_object_or_404(Track, pk=track_id)

    playlist.tracks.remove(track)

    messages.success(request, f'Track "{track.title}" has been removed from your playlist.')
    return redirect('playlist_detail', pk=playlist.pk)


def search_view(request):
    query = request.GET.get('q', '').strip()
    tracks, albums, artists = [], [], []

    if query:
        tracks = Track.objects.filter(title__icontains=query)
        albums = Album.objects.filter(title__icontains=query)
        artists = Artist.objects.filter(name__icontains=query)

        if not tracks.exists() and not albums.exists() and not artists.exists():
            spotify_results = search_spotify(query)

            for item in spotify_results.get('tracks', []):
                import_track(item['id'])

            for item in spotify_results.get('albums', []):
                import_album(item['id'])

            for item in spotify_results.get('artists', []):
                import_artist(item['id'])

            tracks = Track.objects.filter(title__icontains=query)
            albums = Album.objects.filter(title__icontains=query)
            artists = Artist.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'tracks': tracks,
        'albums': albums,
        'artists': artists,
    }
    return render(request, 'music/search_result.html', context)


def add_to_playlist(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    playlist_id = request.GET.get('playlist_id')

    if not playlist_id:
        return HttpResponse("Playlist ID is required.", status=400)

    playlist = get_object_or_404(Playlist, id=playlist_id)

    if track not in playlist.tracks.all():
        playlist.tracks.add(track)
        messages.success(request, f'Added "{track.title}" to the playlist "{playlist.name}".')
    else:
        messages.warning(request, f'"{track.title}" is already in the playlist "{playlist.name}".')

    return redirect('playlist_detail', pk=playlist.id)


class PlaylistNameChangeView(UpdateView):
    model = Playlist
    fields = ['name']
    template_name = 'music/edit_playlist.html'
    context_object_name = 'playlist'

    def get_success_url(self):
        return reverse_lazy('playlist_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)
