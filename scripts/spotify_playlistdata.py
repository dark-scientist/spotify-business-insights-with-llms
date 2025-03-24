import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("❌ Missing Spotify API credentials! Check your .env file.")

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, 
    client_secret=SPOTIFY_CLIENT_SECRET
))

# CSV file (shared format across APIs)
OUTPUT_FILE = "songs.csv"

# Function to fetch all playlist tracks (handling pagination)
def fetch_all_spotify_data(playlist_id):
    try:
        print(f"🔍 Fetching data for Playlist ID: {playlist_id}")
        
        songs = []
        offset = 0
        limit = 100  # Max limit per request

        while True:
            results = sp.playlist_tracks(playlist_id, market="US", limit=limit, offset=offset)

            if not results.get("items"):
                break  # No more tracks, stop fetching

            for item in results["items"]:
                track = item.get("track", {})
                if track:
                    songs.append({
                        "Track Name": track.get("name", "Unknown"),
                        "Artist": track["artists"][0]["name"] if track.get("artists") else "Unknown",
                        "Album": track.get("album", {}).get("name", "Unknown"),
                        "Release Date": track.get("album", {}).get("release_date", "Unknown"),
                        "Popularity": track.get("popularity", 0),
                        "Streams": "N/A",  # Spotify API doesn't provide streams count
                        "Rank": "N/A",  # Rank is not available in Spotify API
                        "Platform": "Spotify",
                        "Source": "Spotify",
                        "Updated At": time.strftime("%Y-%m-%d %H:%M:%S")
                    })

            offset += limit  # Move to the next batch

        return songs

    except spotipy.exceptions.SpotifyException as e:
        print(f"❌ Spotify API Error: {e.http_status} - {e.msg}")
        if e.http_status == 404:
            print("🚨 Playlist not found! Check if the playlist ID is correct.")
        return None
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return None

def append_to_csv(songs):
    if not songs:
        print("⚠️ No song data available to save!")
        return

    df = pd.DataFrame(songs)

    # Ensure consistent CSV format
    csv_columns = ["Track Name", "Artist", "Album", "Release Date", "Popularity", 
                   "Streams", "Rank", "Platform", "Source", "Updated At"]

    if not os.path.exists(OUTPUT_FILE):
        df.to_csv(OUTPUT_FILE, index=False, columns=csv_columns)
    else:
        df.to_csv(OUTPUT_FILE, mode='a', index=False, header=False, columns=csv_columns)

    print(f"✅ {len(songs)} Spotify songs appended to {OUTPUT_FILE}")

# Ask for user input
playlist_url = input("🎵 Enter Spotify Playlist URL: ")
playlist_id = playlist_url.split("/")[-1].split("?")[0]  # Extract playlist ID

# Run the script every 5 minutes
while True:
    song_data = fetch_all_spotify_data(playlist_id)
    append_to_csv(song_data)
    print("🔄 Waiting for the next update...")
    time.sleep(300)  # 5-minute interval
