import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import datetime



load_dotenv()
#Config
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "enter id") 
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "enter secret")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080")
SCOPE = "user-top-read playlist-modify-public playlist-read-private playlist-read-collaborative"#this scope allows for reading top tracks and creating/modifying playlists

"""
Set client variables, called in SpotifyMonthly.py 
"""
def get_spotify_client():

    
    new_sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,         
            client_secret=CLIENT_SECRET, 
            redirect_uri=REDIRECT_URI,  
            scope=SCOPE,
            cache_path=None 
        )
    )
    return new_sp

"""
Get top 20 songs
"""
def get_top_tracks(sp_client):
    #This saves the users top 20 tracks to the temp list top_tracks
    top_tracks = sp_client.current_user_top_tracks(limit=20, time_range='short_term') #'short_term' = last 4 weeks can be changed to 6 months ('medium_term') or all time ('long_term')
    results = [] #empty list to store results
    for item in top_tracks['items']: #iterate through each track item
        track_id   = item['id'] #get track ID
        track_name = item['name'] #get track name 
        artists    = [artist['name'] for artist in item['artists']] #get list of all artists associated with the track
        results.append((track_id, track_name, artists)) #append a tuple of: ( the ID, Song name, Artist(s) Names ) to the results 
    return results

"""
Create playlist with a title and description
"""
def create_and_fill_playlist(sp_client, track_ids, Playlist_name, date_toggle_state):
    user_id = sp_client.current_user()["id"] #get user ID
    name_input = Playlist_name.strip() #.strip() removes any leading/trailing whitespace
   #Date toggle is turned ON
    if date_toggle_state == True:
        #get current month + year 
        current_datetime = datetime.datetime.now()
        date_string = current_datetime.strftime("%B %Y")#make it into a readable string

        if not name_input: #if nothing was entered Playlist name is simply the month + year
            name = f"{date_string}"
        else:
            name = f"{name_input} {date_string}"#Playlist name is user input + month + year
    #Date toggle is turned OFF
    else:
        if not name_input: #if nothing was entered
            name = "My Playlist"#set a default playlistname
        else:
            name = name_input#Users input 

    #Creates Playlist
    playlist = sp_client.user_playlist_create( #playlist has the properties: id, Playlist Name, Public or Private, Playlist Description
        user=user_id, 
        name=name, 
        public=True, 
        description="top 20 songs"
    )
    sp_client.playlist_add_items(playlist_id=playlist["id"], items=track_ids) #track_ids from get_top_tracks() is passed here to add the songs to the playlist
    print(f"Added {len(track_ids)} tracks to playlist: {name}")
