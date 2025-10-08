import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ast
import os

#Config
CLIENT_ID= "enter id"
CLIENT_SECRET= "enter secret"
REDIRECT_URI="http://127.0.0.1:8080"
SCOPE="user-top-read playlist-modify-private playlist-modify-public"

#Authenticate

sp = spotipy.Spotify( #Init spotipy class
    auth_manager=SpotifyOAuth(   
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,  
        scope=SCOPE 
    )
)


"""
Get top 20 songs
"""
def get_top_tracks():
    top_tracks = sp.current_user_top_tracks(limit=20, time_range='short_term')
    results = []
    for item in top_tracks['items']:
        track_id   = item['id']
        track_name = item['name']
        artists    = [artist['name'] for artist in item['artists']]
        results.append((track_id, track_name, artists))
    return results

"""
Create playlist
"""
def create_and_fill_playlist(track_ids):
    user_id = sp.current_user()["id"]
    name    = input("\nEnter a name for your new playlist: ").strip()
    if not name:
        print("Playlist name cannot be empty. Aborting.")
        return
    # Create private playlist
    playlist = sp.user_playlist_create(
        user=user_id, 
        name=name, 
        public=False,
        description="top 20 songs"
    )
    sp.playlist_add_items(playlist_id=playlist["id"], items=track_ids)
    print(f"Added {len(track_ids)} tracks to playlist: {name}")

"""
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
