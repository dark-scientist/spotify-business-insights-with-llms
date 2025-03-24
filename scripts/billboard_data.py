import billboard
import pandas as pd
import os
import datetime

# Path to the shared CSV file
OUTPUT_FILE = "songs.csv"

def fetch_billboard_data(chart_name):  # Removed default "artist-100"
    try:
        print(f"🔍 Fetching Billboard chart: {chart_name}...")
        chart = billboard.ChartData(chart_name)

        # Handle missing chart date
        chart_date = chart.date if chart.date else datetime.date.today().strftime("%Y-%m-%d")

        songs = []
        for entry in chart:
            songs.append({
                "Track Name": entry.title,
                "Artist": entry.artist,
                "Album": "N/A",  # Billboard does not provide album data
                "Release Date": "N/A",  # Billboard does not provide release dates
                "Popularity": "N/A",  # Billboard ranks but no popularity score
                "Streams": "N/A",  # No stream count from Billboard
                "Rank": entry.rank,
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

    # Ensure CSV format remains consistent
    csv_columns = ["Track Name", "Artist", "Album", "Release Date", "Popularity", 
                   "Streams", "Rank", "Platform", "Source", "Updated At"]

    # Append and automatically handle missing headers
    df.to_csv(OUTPUT_FILE, mode='a', index=False, header=not os.path.exists(OUTPUT_FILE), columns=csv_columns)

    print(f"✅ {len(songs)} Billboard entries appended to {OUTPUT_FILE}")

# Fetch and save Billboard data
billboard_data = fetch_billboard_data("artist-100")  # Get Billboard 200 Chart
append_to_csv(billboard_data)
