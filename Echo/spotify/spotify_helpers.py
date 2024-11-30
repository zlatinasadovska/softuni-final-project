from Echo.music.models import Artist, Album, Track
from Echo.spotify.spotify_client import sp


def search_spotify(query):
    """Search for artists, albums, or tracks based on a query."""
    try:
        results = sp.search(q=query, type='track,album,artist', limit=10)
        return {
            'tracks': results.get('tracks', {}).get('items', []),
            'albums': results.get('albums', {}).get('items', []),
            'artists': results.get('artists', {}).get('items', []),
        }
    except Exception as e:
        print(f"Error querying Spotify API: {e}")
        return {'tracks': [], 'albums': [], 'artists': []}


def normalize_release_date(release_date):
    """Normalize the release date to a full date format."""
    if not release_date:
        return None
    return release_date if len(release_date) > 4 else f"{release_date}-01-01"


def import_artist(artist_id):
    """Fetch and save artist details from Spotify."""
    try:
        # Fetch artist data from Spotify
        artist_data = sp.artist(artist_id)
        print(f"Artist Data: {artist_data}")  # Debug the data fetched from Spotify

        # Extract profile picture safely
        profile_picture = artist_data.get('images', [{}])[0].get('url')

        # Create or update the artist object
        artist, created = Artist.objects.update_or_create(
            spotify_id=artist_id,
            defaults={
                'name': artist_data.get('name'),
                'profile_picture': profile_picture,
                'genres': ', '.join(artist_data.get('genres', [])),
                'spotify_url': artist_data.get('external_urls', {}).get('spotify'),
            }
        )
        return artist

    except Exception as e:
        print(f"Error importing artist {artist_id}: {e}")
        return None


def import_album(album_id):
    """Fetch and save album details from Spotify."""
    try:
        # Fetch album data
        album_data = sp.album(album_id)
        print(f"Album Data: {album_data}")  # Debug the data fetched from Spotify

        # Ensure the artist is imported before creating the album
        artist = import_artist(album_data['artists'][0]['id'])
        release_date = normalize_release_date(album_data.get('release_date'))

        # Create or update the album object
        album, created = Album.objects.update_or_create(
            spotify_id=album_id,
            defaults={
                'title': album_data.get('name'),
                'artist': artist,
                'release_date': release_date,
                'cover_image': album_data.get('images', [{}])[0].get('url'),
            }
        )

        # Import tracks from the album
        if album:
            tracks_data = sp.album_tracks(album_id).get('items', [])
            for track in tracks_data:
                import_track(track['id'])

        return album

    except Exception as e:
        print(f"Error importing album {album_id}: {e}")
        return None


def import_track(track_id):
    """Fetch and save track details from Spotify."""
    try:
        # Fetch track data from Spotify API
        track_data = sp.track(track_id)
        print(f"Track Data: {track_data}")  # Debugging output

        # Extract the preview URL (may be None)
        preview_url = track_data.get('preview_url')

        # Import related artist and album
        artist = import_artist(track_data['artists'][0]['id'])
        album = import_album(track_data['album']['id'])

        # Extract track image safely
        track_image = (
            track_data['album']['images'][0]['url']
            if track_data['album'].get('images')
            else None
        )

        # Create or update the track in the database
        track, created = Track.objects.update_or_create(
            spotify_id=track_id,
            defaults={
                'title': track_data['name'],
                'artist': artist,
                'album': album,
                'duration_ms': track_data['duration_ms'],
                'track_image': track_image,
                'preview_url': preview_url,  # Save preview URL (may be None)
            }
        )

        # Debug to confirm if the preview URL was saved
        print(f"Track {track.title} preview URL: {preview_url}")
        return track

    except Exception as e:
        print(f"Error importing track {track_id}: {e}")
        return None
