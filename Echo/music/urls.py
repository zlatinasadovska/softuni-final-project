from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from Echo.music import views
from Echo.music.views import AlbumDetailView, TrackDetailView, PlaylistNameChangeView, give_testimonial, \
    my_testimonials, delete_testimonial

urlpatterns = [
    path('artist/<int:pk>/', views.ArtistDetailView.as_view(), name='artist_detail'),
    path('album/<str:spotify_id>/', AlbumDetailView.as_view(), name='album_detail'),
    path('track/<str:spotify_id>/', TrackDetailView.as_view(), name='track_detail'),
    path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('create_playlist/', views.CreatePlaylistView.as_view(), name='create_playlist'),
    path('delete_playlist/<int:pk>/', views.delete_playlist, name='delete_playlist'),
    path('playlist/<int:playlist_id>/track/<int:track_id>/remove/', views.remove_track_from_playlist,
         name='remove_track_from_playlist'),
    path('search/', views.search_view, name='search'),
    path('add_to_playlist/<int:track_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('playlist/<int:pk>/edit/', PlaylistNameChangeView.as_view(), name='edit_playlist'),
    path('give-testimonial/', give_testimonial, name='give_testimonial'),
    path('my-testimonials/', my_testimonials, name='my_testimonials'),
    path('delete-testimonial/<int:pk>/', delete_testimonial, name='delete_testimonial'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
