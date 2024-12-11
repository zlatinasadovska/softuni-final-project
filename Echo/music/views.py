from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView
from Echo.music.forms import PlaylistForm, TestimonialForm
from Echo.music.models import Artist, Album, Track, Playlist, Testimonial
from Echo.spotify.spotify_helpers import import_track, import_album, search_spotify, import_artist


# View for displaying details of a specific artist
class ArtistDetailView(DetailView):
    model = Artist
    template_name = 'music/artist_details.html'
    context_object_name = 'artist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = self.get_object()

        # Fetch artist data from Spotify if available
        spotify_artist = import_artist(artist.spotify_id)
        if spotify_artist:
            context['spotify_artist'] = spotify_artist
            context['albums'] = spotify_artist.albums.all()
            context['tracks'] = spotify_artist.tracks.all()

        return context


# View for displaying details of a specific album
class AlbumDetailView(DetailView):
    model = Album
    template_name = 'music/album_details.html'
    context_object_name = 'album'

    def get_object(self, queryset=None):
        spotify_id = self.kwargs.get('spotify_id')
        queryset = queryset or self.get_queryset()
        return get_object_or_404(queryset, spotify_id=spotify_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        album = self.get_object()

        tracks = album.tracks.all()

        context['tracks'] = tracks
        return context


# View for displaying details of a specific track
class TrackDetailView(DetailView):
    model = Track
    template_name = 'music/track_details.html'
    context_object_name = 'spotify_track'

    def get_object(self, queryset=None):
        spotify_id = self.kwargs.get('spotify_id')
        track = Track.objects.filter(spotify_id=spotify_id).first()

        if not track:
            track = import_track(spotify_id)
            if not track:
                raise Http404("Track not found or unable to fetch from Spotify.")

        return track

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        track = self.get_object()

        # Calculate and display the track duration in minutes and seconds
        if track.duration_ms:
            duration_minutes = track.duration_ms // 60000
            duration_seconds = (track.duration_ms % 60000) // 1000
            context['duration'] = f"{duration_minutes}:{duration_seconds:02d}"
        else:
            context['duration'] = "Unknown duration"

        context['preview_url'] = track.preview_url

        return context


# View for displaying details of a specific playlist
class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'music/playlist_details.html'
    context_object_name = 'playlist'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()

        sort_order = self.request.GET.get('sort', 'default')

        tracks = playlist.tracks.all()
        if sort_order == 'alphabetical':
            tracks = tracks.order_by('title')
        elif sort_order == 'reverse_alphabetical':
            tracks = tracks.order_by('-title')

        context['tracks'] = tracks
        context['sort_order'] = sort_order
        return context


# View for creating a new playlist, available to logged-in users
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


# View for deleting a playlist
@login_required
def delete_playlist(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
    playlist.delete()
    messages.success(request, "Playlist deleted successfully!")
    return redirect('profile')


# View for removing a track from a playlist
def remove_track_from_playlist(request, playlist_id, track_id):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to perform this action.")

    playlist = get_object_or_404(Playlist, pk=playlist_id)
    track = get_object_or_404(Track, pk=track_id)

    playlist.tracks.remove(track)

    messages.success(request, f'Track "{track.title}" has been removed from your playlist.')
    return redirect('playlist_detail', pk=playlist.pk)


# View for performing a search for tracks, albums, and artists
def search_view(request):
    query = request.GET.get('q', '').strip()
    tracks, albums, artists = [], [], []

    if query:
        # Search in the local database first
        tracks = Track.objects.filter(title__icontains=query)
        albums = Album.objects.filter(title__icontains=query)
        artists = Artist.objects.filter(name__icontains=query)

        # If no results, search in Spotify and import the results
        if not tracks.exists() and not albums.exists() and not artists.exists():
            spotify_results = search_spotify(query)

            for item in spotify_results.get('tracks', []):
                import_track(item['id'])

            for item in spotify_results.get('albums', []):
                import_album(item['id'])

            for item in spotify_results.get('artists', []):
                import_artist(item['id'])

            # Re-fetch the local results after importing from Spotify
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


# View for adding a track to a playlist
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


# View for changing the name of a playlist
class PlaylistNameChangeView(UpdateView):
    model = Playlist
    fields = ['name']
    template_name = 'music/edit_playlist.html'
    context_object_name = 'playlist'

    def get_success_url(self):
        return reverse_lazy('playlist_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        return super().form_valid(form)


# View for submitting a testimonial
@login_required
def give_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            return redirect('home')
    else:
        form = TestimonialForm()

    return render(request, 'music/give_testimonial.html', {'form': form})


# View for displaying all testimonials submitted
@login_required
def my_testimonials(request):
    testimonials = Testimonial.objects.filter(user=request.user)
    return render(request, 'music/my_testimonials.html', {'testimonials': testimonials})


# View for deleting a testimonial
@login_required
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk, user=request.user)
    if request.method == 'POST':
        testimonial.delete()
        return redirect('my_testimonials')
    return render(request, 'music/delete_testimonial.html', {'testimonial': testimonial})
