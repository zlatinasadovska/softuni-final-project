from Echo.music.models import Artist, Album, Track
from Echo.spotify.spotify_client import sp


def search_spotify(query, limit=50, offset=0):
    """Search for artists, albums, or tracks with pagination."""
    try:
        results = sp.search(q=query, type='track,album,artist', limit=limit, offset=offset)
        return {
            'tracks': results.get('tracks', {}).get('items', []),
            'albums': results.get('albums', {}).get('items', []),
            'artists': results.get('artists', {}).get('items', []),
        }
    except Exception as e:
        print(f"Error querying Spotify API: {e}")
        return {'tracks': [], 'albums': [], 'artists': []}


def fetch_all_results(query, limit=50):
    """Fetch all results for a given query with pagination."""
    all_tracks = []
    all_albums = []
    all_artists = []
    offset = 0

    while True:
        results = search_spotify(query, limit=limit, offset=offset)

        all_tracks.extend(results['tracks'])
        all_albums.extend(results['albums'])
        all_artists.extend(results['artists'])

        if len(results['tracks']) < limit and len(results['albums']) < limit and len(results['artists']) < limit:
            break

        offset += limit

    return {
        'tracks': all_tracks,
        'albums': all_albums,
        'artists': all_artists,
    }


def normalize_release_date(release_date):
    """Normalize the release date to a full date format."""
    if not release_date:
        return None
    return release_date if len(release_date) > 4 else f"{release_date}-01-01"


def import_artist(artist_id):
    """Fetch and save artist details from Spotify."""
    try:
        artist_data = sp.artist(artist_id)
        profile_picture = artist_data.get('images', [{}])[0].get('url')

        artist, _ = Artist.objects.update_or_create(
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
        album_data = sp.album(album_id)
        artist = import_artist(album_data['artists'][0]['id'])

        release_date = normalize_release_date(album_data.get('release_date'))

        album, _ = Album.objects.update_or_create(
            spotify_id=album_id,
            defaults={
                'title': album_data.get('name'),
                'artist': artist,
                'release_date': release_date,
                'cover_image': album_data.get('images', [{}])[0].get('url'),
            }
        )
        return album
    except Exception as e:
        print(f"Error importing album {album_id}: {e}")
        return None


def import_track(track_id):
    """Fetch and save track details from Spotify."""
    try:
        track_data = sp.track(track_id)

        preview_url = track_data.get('preview_url')
        spotify_url = track_data.get('external_urls', {}).get('spotify')

        print(f"Track {track_id} - Preview URL: {preview_url}")

        artist = import_artist(track_data['artists'][0]['id'])
        album = import_album(track_data['album']['id'])

        track_image = track_data['album']['images'][0].get('url') if track_data['album'].get('images') else None

        track, created = Track.objects.update_or_create(
            title=track_data['name'],
            artist=artist,
            defaults={
                'spotify_id': track_id,
                'album': album,
                'duration_ms': track_data['duration_ms'],
                'track_image': track_image,
                'spotify_url': spotify_url,
                'preview_url': preview_url,
            }
        )

        if created:
            print(f"Successfully imported track: {track_data['name']}")
        return track

    except Exception as e:
        print(f"Error importing track {track_id}: {e}")
        return None
