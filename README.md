# Spotify Monthly

A Python script that uses the Spotify Web API to fetch your current top 20 tracks (short-term, last 4 weeks) and automatically creates a new playlist with them. It also saves your top artists for analysis.
---
## Features

* **Fetch Top Tracks:** Retrieves your **top 20 tracks** from the last four weeks (`short_term` time frame).
* **Playlist Creation:** Creates a **new** Spotify playlist with the fetched tracks, prompting the user for a playlist name.
* **Artist Analysis:** Saves the track names and associated artists to `artist_list.txt` and then counts the occurrences of each artist, saving the sorted results to `artist_count.txt`. 

---

## Installation and Setup

### Prerequisites

* **Python 3.x**
* A **Spotify Developer Account** to obtain your `CLIENT_ID` and `CLIENT_SECRET`.

### 1. Clone the Repository

```bash
git clone https://github.com/mheathcock/SpotifyMonthly.git
cd SpotifyMonthly
```

### 2. Install Dependencies

This project relies on the `spotipy` library. Install it using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```


## Currently Working On

* Functionality to allow **any user** to use the app **without** the need for personal Spotify Developer App setup (simplifying the setup).
* Functionality to save each monthly recap into a growing file for end of year analysis *(A basic Spotify Wrapped style summary)*.
* **GUI Functionality:** Developing a graphical user interface (GUI) to replace the current command-line interface (CLI) for easier, more intuitive use.
