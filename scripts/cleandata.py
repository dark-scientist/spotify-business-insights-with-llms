import pandas as pd

# Load the dataset
file_path = "songs.csv"
df = pd.read_csv(file_path)

print("\n🔍 Initial Data Overview:")
print(df.info())
print(df.head())

# Drop duplicates while keeping the latest entry
df.drop_duplicates(subset=["Track Name", "Artist", "Platform"], keep="last", inplace=True)

# Fill missing values appropriately
df.fillna({
    "Track Name": "Unknown",
    "Artist": "Unknown",
    "Album": "Unknown",
    "Release Date": "N/A",
    "Popularity": 0,
    "Streams": 0,
    "Rank": "N/A",
    "Platform": "Unknown",
    "Source": "Unknown"
}, inplace=True)

# Convert numeric fields to integers (handling errors safely)
df["Popularity"] = pd.to_numeric(df["Popularity"], errors="coerce").fillna(0).astype(int)
df["Streams"] = pd.to_numeric(df["Streams"], errors="coerce").fillna(0).astype(int)

# Standardize text formatting (strip spaces & apply title case)
df["Track Name"] = df["Track Name"].str.strip().str.title()
df["Artist"] = df["Artist"].str.strip().str.title()
df["Platform"] = df["Platform"].str.strip().str.upper()
df["Source"] = df["Source"].str.strip().str.upper()

# Drop completely empty columns (if any)
df.dropna(axis=1, how='all', inplace=True)

# Save the cleaned data
cleaned_file_path = "songs_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

print("\n✅ Data cleaning complete! Saved as 'songs_cleaned.csv'.")
