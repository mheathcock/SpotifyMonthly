from main import *
from tkinter import *
from tkinter import messagebox 
import customtkinter as CTk
from PIL import Image, ImageTk
from auth import *
app = CTk.CTk()
app.geometry("1920x1080")
app.configure(bg="#121212")
app.state('zoomed')  


"""
Front end GUI for user authentication.
"""
def login_gui():
    #forget previous widgets
    for widget in app.winfo_children():
        widget.destroy()
    
  
    app_frame = CTk.CTkFrame(app, fg_color="transparent")
    app_frame.pack(expand=True,anchor="center")

    app.title("Login")
    
   
    CTk.CTkButton(
        app_frame, 
        text="Login", 
        command=login_gui, 
        width=250, 
        height=50, 
        font=CTk.CTkFont(family="Helvetica Neue LT Std",size=30, weight="bold"),
        corner_radius=30,
        fg_color="#BB86FB", 
        hover_color="#9C5AF7"
    ).pack(pady=10)
     


"""
Front end GUI for logging in the User
"""
def login_gui():
    #Forget previous widgets
    for widget in app.winfo_children():
        widget.destroy()
    
    app.title("Login")
    
    CTk.CTkButton(
        app, 
        text="Back", 
        width=100, 
        height=30, 
        command=login_gui,
        fg_color="gray", 
        hover_color="darkgray"
    ).pack(side="top", anchor="nw", pady=10, padx=10)#Back button to return to login/register choice screen
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
    CTk.CTkButton(
        login_frame, 
        text="SUBMIT",
        font=CTk.CTkFont(family="Helvetica Neue LT Std",size=40, weight="bold"),
        text_color="white",
        width=200, 
        height=50, 
        corner_radius=35,
        fg_color="black", 
        hover_color="#333333",
        command=start_spotify_login
    ).pack(pady=(20, 5))
  

  
"""
Main GUI Function for the app, is called once user is 
logged in and uses their credentials to set the config files and call the functions to display spotify info
"""      
def MainGUI(spotify_client):
    #Forget previous widgets
    for widget in app.winfo_children():
        widget.destroy()
    app.title("Main Application Dashboard")

    #Create a central frame to hold all content
    main_frame = CTk.CTkFrame(app, fg_color="transparent")
    main_frame.pack(expand=True, fill="both")
    
    try:
        user_info = spotify_client.current_user()
        username = user_info.get('display_name', 'Your Friend')
        

        CTk.CTkLabel(
            main_frame, 
            text=f"Welcome, {username}! Viewing Top Tracks.", 
            font=CTk.CTkFont(family="Helvetica Neue LT Std", size=40, weight="bold"),
            text_color="#BB86FB"
        ).pack(pady=(40, 20))
        
        display_top_tracks(main_frame, spotify_client) 
        
    except Exception as e:
        messagebox.showerror("Authentication Error", f"Access denied or token expired: {e}")
        login_gui()
    """
    Fetches top tracks, formats them, and displays them in a CTkTextbox.
    """
def display_top_tracks(app_frame, spotify_client):

    
    try:
        raw_tracks = get_top_tracks(spotify_client)
    except Exception as e:
        messagebox.showerror("Spotify API Error", f"Could not fetch top tracks: {e}")
        return
    formatted_output = "YOUR TOP 20 TRACKS (of the last 4 Weeks) \n\n"
    
    if not raw_tracks:
        formatted_output += "No recent track data found for this account."
    else:
        for i, (track_id, track_name, artists) in enumerate(raw_tracks):
            artists_str = ", ".join(artists)
            formatted_output += f"{i+1}. {track_name} — {artists_str}\n"

    track_textbox = CTk.CTkTextbox(
        master=app_frame,
        width=800,
        height=500,
        font=CTk.CTkFont(family="Arial", size=18),
        fg_color="#1F1F1F", 
        text_color="white",
        wrap="word" #Wrap long lines
    )
    track_textbox.pack(pady=20, padx=20, fill="both", expand=True)

 
    track_textbox.insert("0.0", formatted_output)
    
 
    track_textbox.configure(state="disabled")   #Make the textbox read-only after insertion


login_gui()
app.mainloop()

