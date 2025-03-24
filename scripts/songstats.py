import requests
import pandas as pd
import os
import time
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API credentials from .env file
API_KEY = os.getenv("RAPIDAPI_KEY", "3635efa2aemsh9a61d2bdbb09a30p153c1fjsnf960fe84bd12")  # Ensure to set this in your .env
API_HOST = "songstats.p.rapidapi.com"
ENDPOINT = "https://songstats.p.rapidapi.com/collaborators/stats"

# Parameters for Songstats API
QUERY_PARAMS = {
    "source": "all",
    "tidal_artist_id": "49475872",  # Replace with actual artist ID
    "songstats_collaborator_id": "kvWh40q1"  # Replace with actual collaborator ID
}

HEADERS = {
    "x-rapidapi-host": "songstats.p.rapidapi.com",
    "x-rapidapi-key": "2308bae965msh2deb659731ab315p16c59ajsncc33b8c8d3dc"
}

# Path to the CSV file
OUTPUT_FILE = "songs.csv"

def fetch_songstats_data():
    """Fetches live song stats from Songstats API."""
    try:
        logging.info("🔍 Fetching live song stats...")
        response = requests.get(ENDPOINT, headers=HEADERS, params=QUERY_PARAMS)

        if response.status_code == 403:
            logging.error("❌ API Error 403: Subscription issue or invalid API key!")
            return None
        elif response.status_code != 200:
            logging.error(f"❌ API Error {response.status_code}: {response.text}")
            return None

        data = response.json()
        songs = []

        if "data" in data:
            for item in data["data"]:
                songs.append({
                    "Track Name": item.get("track_name", "Unknown"),
                    "Artist": item.get("artist_name", "Unknown"),
                    "Album": "N/A",  # Songstats does not provide album info
                    "Release Date": "N/A",  # Not available from Songstats
                    "Popularity": "N/A",  # No popularity metric in Songstats
                    "Streams": item.get("streams", 0),
                    "Rank": item.get("rank", "N/A"),
                    "Platform": item.get("platform", "Unknown"),
                    "Source": "Songstats",
                    "Updated At": time.strftime("%Y-%m-%d %H:%M:%S")
                })

        return songs

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Request Error: {e}")
        return None
    except Exception as e:
        logging.error(f"❌ Unexpected Error: {e}")
        return None

def append_to_csv(songs):
    """Appends song data to a CSV file."""
    if not songs:
        logging.warning("⚠️ No song data available to save!")
        return

    df = pd.DataFrame(songs)

    # Ensure CSV format remains consistent
    csv_columns = ["Track Name", "Artist", "Album", "Release Date", "Popularity", 
                   "Streams", "Rank", "Platform", "Source", "Updated At"]

    if not os.path.exists(OUTPUT_FILE):
        df.to_csv(OUTPUT_FILE, index=False, columns=csv_columns)
    else:
        df.to_csv(OUTPUT_FILE, mode='a', index=False, header=False, columns=csv_columns)

    logging.info(f"✅ {len(songs)} song stats appended to {OUTPUT_FILE}")

def main():
    """Runs the script every 5 minutes with retry logic."""
    while True:
        song_data = fetch_songstats_data()
        append_to_csv(song_data)
        logging.info("🔄 Waiting for next update...")
        time.sleep(300)  # 5-minute interval

if __name__ == "__main__":
    main()
