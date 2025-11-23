from main import *
from tkinter import *
from tkinter import messagebox 
import customtkinter as CTk
from PIL import Image, ImageTk
import datetime

app = CTk.CTk()
app.geometry("1920x1080")
app.configure(bg="#121212")
app.state('zoomed')  

#Variable for setting a boolean that determines if the Users playlist should contain a month + year
date_toggle_var = CTk.BooleanVar(value=True)
track_ids = []


"""
Front end GUI for logging in the User
"""
def login_gui():
    #Forget previous widgets
    for widget in app.winfo_children():
        widget.destroy()
    
    app.title("Login")
    

    main_Frame = CTk.CTkFrame(
        master=app,
        fg_color="#BB86FB",
        corner_radius=150,
        border_width=0
    )
    main_Frame.pack(expand=True, fill='x', anchor="center", padx=500)

    login_frame = CTk.CTkFrame(
        master = main_Frame,
        fg_color="transparent"
        ) 
    #Center the frame in the window
    login_frame.pack(expand=True, fill="both", padx=50, pady=50)
    

    """
    Main function to allow a user to login to their spotify account
    """
    def start_spotify_login():  
        try:
            spotify_client = get_spotify_client() 
            MainGUI(spotify_client) #Pass the fully authenticated client to the main screen
        
        except Exception as e:
            messagebox.showerror("Login Error", f"Failed to connect to Spotify. Error: {e}")
            login_gui() #Return to the start
       

    #Login button that calls the start_spotify_login function when clicked
    Login_button = CTk.CTkButton(
        login_frame, 
        text="LOGIN TO SPOTIFY",
        font=CTk.CTkFont(family="Helvetica Neue LT Std",size=40, weight="bold"),
        text_color="white",
        width=200, 
        height=50, 
        corner_radius=35,
        fg_color="black", 
        hover_color="#333333",
        command=start_spotify_login
    )
    Login_button.pack(pady=(20, 5))
    
"""
Main GUI Function for the app, is called once user is 
logged in asking them if they want to view top tracks or analyse playlists
"""       
def MainGUI(spotify_client):
    for widget in app.winfo_children():
        widget.destroy()
    app.title("Dashboard")    
    main_frame = CTk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(expand=True, fill="both")
    CTk.CTkButton(
        main_frame, 
        text="Back", 
        width=100, 
        height=30, 
        command=login_gui,
        fg_color="gray", 
        hover_color="darkgray"
    ).pack(side="top", anchor="nw", pady=10, padx=10)#Back button to return to login screen
    
    button_container = CTk.CTkFrame(main_frame, fg_color="transparent")
    button_container.pack(pady=50, expand=True, anchor="center")

    view_track_button = CTk.CTkButton(
        master=button_container, 
        text="View Tracks", 
        width=250, 
        height=50, 
        font=CTk.CTkFont(family="Helvetica Neue LT Std",size=30, weight="bold"),
        corner_radius=30,
        fg_color="#BB86FB", 
        hover_color="#9C5AF7",
        text_color="white",
        command=lambda: Show_Track_GUI(spotify_client)
    )
    view_track_button.pack(side='left', padx=15, pady=10)
   
    analyse_track_button = CTk.CTkButton(
        master=button_container, 
        text="Analyse Tracks", 
        width=250, 
        height=50, 
        font=CTk.CTkFont(family="Helvetica Neue LT Std",size=30, weight="bold"),
        corner_radius=30,
        fg_color="#BB86FB", 
        hover_color="#9C5AF7",
        text_color="white",
        command=lambda: Analyse_Track_GUI(spotify_client)
    )
    analyse_track_button.pack(side='right', padx=15, pady=10)
  
  
"""
Show Track GUI function that will show the user their top 20 tracks and allow them to create a playlist of these tracks
""" 
def Show_Track_GUI(spotify_client):


    global Playlist_entry_name
  
   

    #Forget previous widgets
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Your Top 20 Tracks")

    #Create a central frame to hold all content
    main_frame = CTk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(expand=True, fill="both")
   
    #Back button
    CTk.CTkButton(
        master=main_frame, 
        text="Back", 
        width=100, 
        height=30, 
        command=lambda: MainGUI(spotify_client),
        fg_color="gray", 
        hover_color="darkgray"
    ).pack(side="top", anchor="nw", pady=10, padx=10)

    try:
        user_info = spotify_client.current_user()
        username = user_info.get('display_name', '')
        

        CTk.CTkLabel(
            main_frame, 
            text=f"Welcome, {username}! Viewing Top Tracks.", 
            font=CTk.CTkFont(family="Helvetica Neue LT Std", size=40, weight="bold"),
            text_color="#BB86FB"
        ).pack(pady=(40, 20))
   
    except Exception as e:
        messagebox.showerror("Authentication Error", f"Access denied or token expired: {e}")
        login_gui()
    
    content_frame  = CTk.CTkFrame(
        main_frame,
        fg_color="transparent"
    )
    content_frame.pack(fill="both", expand=True, padx=20, pady=10)

    content_frame.grid_columnconfigure(0, weight=3)
    content_frame.grid_columnconfigure(1, weight=1)
    content_frame.grid_rowconfigure(0, weight=1)

    display_top_tracks(content_frame, spotify_client) 

    controls_frame = CTk.CTkFrame(
        content_frame,
        fg_color="transparent"
    )
    controls_frame.grid(row=0, column=1, padx=20, pady=20, sticky="n")
    
    
    CTk.CTkLabel(
            controls_frame, 
            text=f"Write a name for your Playlist!", 
            font=CTk.CTkFont(family="Helvetica Neue LT Std", size=20, weight="bold"),
            text_color="#BB86FB"
        ).pack(pady=(20, 10))
    
    #Switch responsible for letting the user choose if they want the playlist name to include current month + year
    CTk.CTkSwitch(
        master=controls_frame,
        text="Add current Month + Year for analysis functions",
        font=CTk.CTkFont(size=16),
        fg_color="#1B1A1B", #Colour for OFF
        progress_color="#BB86FB", #Colour for ON
        variable=date_toggle_var, 
        onvalue=True,
        offvalue=False
    ).pack(pady=(5, 15), padx=50)

    #Entry box for the user to input a playlist name
    Playlist_entry_name = CTk.CTkEntry(
    master=controls_frame,
    placeholder_text="Enter Playlist Name",
    font=CTk.CTkFont(family="Helvetica Neue LT Std",size=30, weight="normal"),
    width=450,
    height=60,
    corner_radius=30, 
    fg_color="white",
    text_color="#171717",
    border_width=0
    )
    Playlist_entry_name.pack(pady=(20, 10), padx=50)

    CTk.CTkButton(
        master=controls_frame, 
        text="Create Playlist", 
        width=250, 
        height=50, 
        font=CTk.CTkFont(family="Helvetica Neue LT Std",size=30, weight="bold"),
        corner_radius=30,
        fg_color="#BB86FB", 
        hover_color="#9C5AF7",
        text_color="white",
        command=lambda: save_playlist(spotify_client)
    ).pack(pady=10)

"""Logic function for saving the playlist to users Spotify account"""
def save_playlist(spotify_client):
    global Playlist_entry_name, track_ids,date_toggle_var 

    playlist_name = Playlist_entry_name.get() #get the name the user inputted in Show_Track_GUI - Playlist_entry_name CTk Entry
    add_date_to_name = date_toggle_var.get()

    if playlist_name == "":
        if add_date_to_name:
            messagebox.showerror("Warning!", "No Playlist name entered, default will be the current month + year")
        else:
            messagebox.showerror("Warning!", "No Playlist name entered, default will be 'My Playlist'")

        Playlist_entry_name.configure(border_color="red", border_width=3)
      
    
    if not track_ids:
        messagebox.showwarning("Warning!", "No top tracks were retrieved. Cannot fill playlist.")
        return
    
    try:
        create_and_fill_playlist(spotify_client, track_ids, playlist_name, add_date_to_name)#Call function from main.py that will create and populate the playlist with the top 20 tracks
    except Exception as e:
        messagebox.showerror("Spotify API Error", f"Could not create playlist: {e}")
    else:
        messagebox.showinfo("Success!", "Playlist created!")
        Playlist_entry_name.configure(border_color="#9C5AF7", border_width=0)
        Playlist_entry_name.delete(0, CTk.END)


    """
    Fetches top tracks, formats them, and displays them in a CTkTextbox.
    """
def display_top_tracks(app_frame, spotify_client):
    global track_ids
    
    try:
        raw_tracks = get_top_tracks(spotify_client)
        
    except Exception as e:
        messagebox.showerror("Spotify API Error", f"Could not fetch top tracks: {e}")
        return
    formatted_output = "YOUR TOP 20 TRACKS (of the last 4 Weeks) \n\n"
    
    if not raw_tracks:
        formatted_output += "No recent track data found for this account."
    else:
        track_ids = [item[0] for item in raw_tracks]
        for i, (track_id, track_name, artists) in enumerate(raw_tracks):
            artists_str = ", ".join(artists)
            formatted_output += f"{i+1}. {track_name} — {artists_str}\n"

    track_textbox = CTk.CTkTextbox(
        master=app_frame,
        width=500,
        height=500,
        font=CTk.CTkFont(family="Helvetica Neue LT Std", size=18),
        fg_color="#1F1F1F", 
        text_color="white",
        wrap="word" #Wrap long lines
    )
    track_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

 
    track_textbox.insert("0.0", formatted_output)
    
 
    track_textbox.configure(state="disabled")   #Make the textbox read-only after insertion

"""
Logic for analysing the tracks.
 This is based on if the user has been saving playlists with the year attached as this will be the filter
 """
def analyse_track(spotify_client):
    
  
    all_playlists = []
    
     #Uses pagination for playlists
    results = spotify_client.current_user_playlists(limit=50)  #Fetch inital page
    all_playlists.extend(results.get('items', []))#Extend the list to all these fetched playlists
    
    #Loop as long as Spotify indicates there is a 'next' page
    while results.get('next'):
        try:
            results = spotify_client.next(results)
            all_playlists.extend(results.get('items', []))
            
        except Exception:
           #Fail on error during pagination rather than crashing the GUI
            break


    current_year = datetime.datetime.now().year#use the current year as our filter
    
    #once all playlists from user have been searched apply filter to get the relevant playlists for analysis
    target_playlists = [
        p for p in all_playlists 
        
        if isinstance(p, dict) and #ensure p is a dict
        #check if the filter (current year) is in the playlist name
        f"{current_year}" in p.get('name', '').upper()# ('name', '') will default to empty string if playlist is missing a name preventing keyerror
    ]
    
   
    
    artist_counts = {}
    
    for playlist in target_playlists:
        tracks_results = spotify_client.playlist_items(playlist['id']) #Fetch the first page of tracks for the current playlist
        
        #Aggregate all tracks for this playlist use pagination 
        all_tracks = tracks_results.get('items', [])#default 100 tracks
        
        #Loop as long as Spotify indicates there is a 'next' page of tracks
        while tracks_results.get('next'):
            try:
                tracks_results = spotify_client.next(tracks_results)
                all_tracks.extend(tracks_results.get('items', []))
            except Exception:
                #Fail on track pagination error
                break
            
        #Count artists from ALL retrieved tracks
        for item in all_tracks:
            #Safely check if track key exists to skip local files or null tracks
            track_data = item.get('track')
            if track_data and track_data.get('artists'):#Check that the track data is valid and has an 'artists' list
                for artist in track_data['artists']:#Iterates through every artist assosciated incase of collab or features 
                    artist_name = artist['name']#Extract artist(s) name
                    artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1 #count is 0 if artist is new 
                    
    #Sort and return results
    top_artists = sorted(artist_counts.items(), key=lambda item: item[1], reverse=True)
    return top_artists

"""
GUI for displaying these analysed artists
"""
def Analyse_Track_GUI(spotify_client):
    #Forget previous widgets
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Analyse Tracks")

    main_frame = CTk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(expand=True, fill="both")
    #Back button 
    CTk.CTkButton(
        master=main_frame, 
        text="Back", 
        width=100, 
        height=30, 
        command=lambda: MainGUI(spotify_client),
        fg_color="gray", 
        hover_color="darkgray"
    ).pack(side="top", anchor="nw", pady=10, padx=10)

    #Loading message as analysis takes time
    loading_label = CTk.CTkLabel(
        master=main_frame,
        text="Analysing Playlists...", 
        font=CTk.CTkFont(family="Helvetica Neue LT Std", size=25, weight="bold"),
        text_color="#BB86FB"
    )
    loading_label.pack(pady=(200, 20))
    app.update() #Force the GUI to update and show the loading message immediately

    #Start analysis func
    try:
        output = analyse_track(spotify_client)#call the function that handles analysing playlists based of current year filter
    except Exception as e:
        messagebox.showerror("Analysis Error", f"An error occurred during analysis: {e}")
        MainGUI(spotify_client)
        return

    loading_label.destroy()#Remove loading message

    

    CTk.CTkLabel(
        master=main_frame,
        text=f"YOUR TOP ARTISTS FROM RECAP PLAYLISTS\n",
        font=CTk.CTkFont(family="Helvetica Neue LT Std", size=25, weight="bold"),
        text_color="#BB86FB"
        ).pack(pady=(20, 10))


    

    formatted_output = ""
    if not output:#if the user hasn't been using the toggle for appending the month + year there will be no tracks to analyse
        formatted_output += "\n No artists found in the target playlists."
    else:
        for i, (artist_name, count) in enumerate(output):
            formatted_output += f"\n {i+1}. {artist_name} ({count} tracks)\n"

    track_textbox = CTk.CTkTextbox(
        master=main_frame,
        width=500,
        height=800,
        font=CTk.CTkFont(family="Helvetica Neue LT Std", size=18),
        fg_color="#1F1F1F", 
        text_color="white",
        wrap="word" #Wrap long lines
    )
    track_textbox.pack(padx=20, pady=20, fill="y", expand=True)

 
    track_textbox.insert("0.0", formatted_output)
    
 
    track_textbox.configure(state="disabled")
    
    

login_gui()
app.mainloop()



