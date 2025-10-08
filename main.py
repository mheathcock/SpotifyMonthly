import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ast
import os

#Config
CLIENT_ID= os.environ.get('CLIENT_ID')
CLIENT_SECRET= os.environ.get('CLIENT_ID')
REDIRECT_URI="http://localhost:8888/callback"
SCOPE="user-top-read playlist-modify-private playlist-modify-public playlist-read-private playlist-read-public"

#Authenticate

sp = spotipy.Spotify( #Init spotipy class
    auth_manager=SpotifyOAuth(   
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,  
        scope=SCOPE 
    )
)



def get_top_tracks():
    top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
    results = []
    for item in top_tracks['items']:
        track_id   = item['id']
        track_name = item['name']
        artists    = [artist['name'] for artist in item['artists']]
        results.append((track_id, track_name, artists))
    return results

