# Spotify Monthly
A simple desktop application built with **Python** and **Tkinter** designed to help Spotify users capture and analyse their recent listening habits.

***

## Key Features

* **Top Track Fetching:** Connects to the **Spotify Web API** to fetch and display your **current top 20 tracks** (based on a short-term range: the last 4 weeks of listening).
* **Custom Playlist Creation:** Users have the option to save these 20 tracks directly to a new playlist with a **custom name** of their choice.
* **Analysis Toggle:** Includes a toggle to append the current **Month and Year** to the playlist name (e.g., "Monthly Recap May 2025"). This is essential for utilising the data analysis feature.
* **Top Artist Analysis:** A separate function analyses all user-created playlists containing the **current year in the title**. This process counts all tracks across these playlists to determine and display the user's overall **most-played artists** for the year so far.


## Installation and Setup

### Prerequisites

* **Python 3.x**
*  **Spotify Developer Credentials:** The app requires a `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` to be set as environment variables (or in a `.env` file) to authenticate with the Spotify API. 

### 1. Clone the Repository

```bash
git clone https://github.com/mheathcock/SpotifyMonthly.git
cd SpotifyMonthly
```

### 2. Install Dependencies

* This project relies on the `spotipy` library. Install it using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### 3. Configure Credentials

1. **Create the File:** Copy the provided example file (`example env.env`), rename it to `.env`
   * **Linux/macOS/Git Bash:**
        ```bash
        cp "example env.env" .env
        ```
    * **Windows Command Prompt (CMD):**
        ```bash
        copy "example env.env" .env
        ```
2.  **Populate Variables:**
    Open the newly created **`.env`** file and replace the placeholder values (`<YOUR_CLIENT_ID_HERE>`, etc.) with your actual Spotify Developer credentials.

### 4. Run the Application

Execute the main application file from the project directory:

```bash
python SpotifyMonthly.py
```

## Currently Working On
### Completed
  
* **GUI Implemented:** The application now utilizes a full graphical user interface (GUI), replacing the initial command-line interface (CLI) for a more intuitive user experience.
* **Simplified Authentication:** The application uses **Spotify's secure OAuth 2.0 flow** to handle all token generation and caching automatically, ensuring a smooth, persistent connection without manual token management.

### Future Development
  
* Adding more **visualization** to the analysis results (e.g., charts or graphs for top artists).
* Develop a **backup or export feature** for analysis data (e.g., CSV export of top artists).
* **Implement PKCE Authentication:** Refactor the Spotify OAuth flow to use the PKCE method, allowing the application to run **without requiring users to manually input a Client Secret**.
* **Application Packaging:** Package the Python application into standalone executables for distribution on Windows and macOS.
* **Secure Token Management:** Implement a solution for securely storing the user's Spotify refresh token on the operating system.
