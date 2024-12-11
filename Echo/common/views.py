from django.db.models import Q
from django.views import View
from django.shortcuts import render
from Echo.music.models import Artist, Testimonial


# Main view for the homepage, responsible for fetching featured artists and testimonials
class HomeView(View):
    def get(self, request, *args, **kwargs):
        artists_with_albums_or_tracks = Artist.objects.filter(
            Q(albums__isnull=False) | Q(tracks__isnull=False)
        ).distinct()

        artist_ids = artists_with_albums_or_tracks.values_list('id', flat=True)
        featured_artists = Artist.objects.filter(id__in=artist_ids).order_by('?')[:5]

        testimonials = Testimonial.objects.all().order_by('-id')[:3]

        context = {
            'featured_artists': featured_artists,
            'testimonials': testimonials,
        }

        return render(request, 'common/home.html', context)
