import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

# Path to save CSV
OUTPUT_FILE = "songs.csv"

# Billboard 200 Chart URL
BILLBOARD_URL = "https://www.billboard.com/charts/digital-song-sales/"

def fetch_billboard_200():
    try:
        print(f" Fetching Billboard 200 chart...")
        response = requests.get(BILLBOARD_URL, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print(f"❌ Error: Received status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        chart_date = datetime.date.today().strftime("%Y-%m-%d")

        songs = []
        chart_entries = soup.select("li.o-chart-results-list__item")  # Selects chart list items

        for index, entry in enumerate(chart_entries, start=1):
            title_tag = entry.select_one("h3")  # Song title
            artist_tag = entry.select_one("span")  # Artist name

            if title_tag and artist_tag:
                title = title_tag.text.strip()
                artist = artist_tag.text.strip()

                songs.append({
                    "Track Name": title,
                    "Artist": artist,
                    "Album": "N/A",
                    "Release Date": "N/A",
                    "Popularity": "N/A",
                    "Streams": "N/A",
                    "Rank": index,
                    "Platform": "Billboard",
                    "Source": "Billboard",
                    "Updated At": chart_date
                })

        return songs

    except Exception as e:
        print(f"❌ Error fetching Billboard data: {e}")
        return None

def append_to_csv(songs):
    if not songs:
        print("⚠️ No Billboard data to save!")
        return

    df = pd.DataFrame(songs)
    csv_columns = ["Track Name", "Artist", "Album", "Release Date", "Popularity", 
                   "Streams", "Rank", "Platform", "Source", "Updated At"]

    df.to_csv(OUTPUT_FILE, mode='a', index=False, header=not pd.io.common.file_exists(OUTPUT_FILE), columns=csv_columns)
    print(f"✅ {len(songs)} Billboard entries appended to {OUTPUT_FILE}")

# Fetch and save Billboard 200 data
billboard_data = fetch_billboard_200()
append_to_csv(billboard_data)
