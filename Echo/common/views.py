from django.db.models import Q
from django.views import View
from django.shortcuts import render
from Echo.music.models import Artist


class HomeView(View):
    def get(self, request, *args, **kwargs):
        # Step 1: Fetch artists who have either at least one album or one track
        # This fetches artists who have either albums or tracks
        artists_with_albums_or_tracks = Artist.objects.filter(
            Q(albums__isnull=False) | Q(tracks__isnull=False)  # Artists with albums OR tracks
        ).distinct()

        # Step 2: Randomly select 5 unique artists (ensure no duplicates)
        # Get the IDs of those artists to avoid any duplicates in the selection
        artist_ids = artists_with_albums_or_tracks.values_list('id', flat=True)

        # Randomly pick 5 distinct artist IDs and fetch the corresponding artists
        featured_artists = Artist.objects.filter(id__in=artist_ids).order_by('?')[:5]

        context = {
            'featured_artists': featured_artists,
        }

        return render(request, 'common/home.html', context)
