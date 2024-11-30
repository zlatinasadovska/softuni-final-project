import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from Echo.spotify.spotify_config import CLIENT_ID, CLIENT_SECRET

client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
