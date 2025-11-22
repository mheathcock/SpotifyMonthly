import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ast
import os
import os
from dotenv import load_dotenv

load_dotenv()
#Config
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "enter id") 
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "enter secret")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080")
SCOPE="user-top-read playlist-modify-private playlist-modify-public"#this scope allows for reading top tracks and creating/modifying playlists

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
def create_and_fill_playlist(sp_client, track_ids):
    user_id = sp_client.current_user()["id"] #get user ID
    name    = input("\nEnter a name for your new playlist: ").strip() #.strip() removes any leading/trailing whitespace
    if not name: #if nothing was entered
        print("Playlist name cannot be empty. Aborting.") 
        return
    #Creates Playlist
    playlist = sp_client.user_playlist_create( #playlist has the properties: id, Playlist Name, Public or Private, Playlist Description
        user=user_id, 
        name=name, 
        public=False, #private playlist
        description="top 20 songs"
    )
    sp_client.playlist_add_items(playlist_id=playlist["id"], items=track_ids) #track_ids from get_top_tracks() is passed here to add the songs to the playlist
    print(f"Added {len(track_ids)} tracks to playlist: {name}")

"""
Rework started to implement these into the GUI for data analysis 


Write the artist list to a text file 
"""
def write_artist_list(artist_list, file_path):
    artist = [name[-2:] for name in artist_list]#removes the track ID and instead just keeps the name and artist
    with open(file_path, 'a', encoding='utf-8') as file: #opens file in append mode
        for song_artist in artist:#iterates through the artist list 
           file.write("".join(str(song_artist)) + '\n')#writes each song + artist to a new line
        print("Saved")
"""
Read the artist list from a text file and count occureneces of artists
"""
def read_artist_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as file: # Opens file in read mode
        Artist_dict = {} # empty dictionary to store the artist : count 
        Artist = [] #empty list to store artist names as they are read from the file
        
        for line in file: # for each line in the text file
            track_name, artist_list = ast.literal_eval(line.strip()) # converts string representation of list back to actual list
            for artist_name in artist_list: #iterate through each artist in the list
                if artist_name in Artist: # if the artist is already been seen
                    Artist_dict[artist_name] += 1 #add +1 to that artist's count in the dictionary
                else: # the artist hasnt been seen yet
                    Artist.append(artist_name) # add this artist to the list of artists as it has now been seen
                    Artist_dict[artist_name] = 1 # add the artist to the dictionary and set its count to 1
        
        sorted_artists = sorted(Artist_dict.items(), key=lambda x: x[1], reverse=True) #sort the dictionary by count in descending order
        lines = [f"{artist}: {count}" for artist, count in sorted_artists] # format dictionary items into string as "artist: count"
        return '\n'.join(lines) # add a new line between each artist
    

if __name__ == "__main__":
    top20=get_top_tracks()#get the tracks
    save = input("\nWould you like to save these to a new private playlist? (y/n): ").strip().lower()#ask user if they want to save the tracks
    if save == 'y':
        write_artist_list(top20, 'artist_list.txt')#save this data to a file to use for analysis
        with open('artist_count.txt', 'w', encoding='utf-8') as file:
            file.write(str(read_artist_list('artist_list.txt')))
        track_ids = [item[0] for item in top20]#gather track ids
        create_and_fill_playlist(track_ids)#create into playlist
    else:
        pass
