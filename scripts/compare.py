import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
file_path = "songs_cleaned.csv"
df = pd.read_csv(file_path)

# Convert Rank to numeric for analysis (handle "N/A" cases)
df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")

print("\n Basic Data Insights:")
print(df.describe())

#  Top 10 Artists with Most Songs in the Chart**
top_artists = df["Artist"].value_counts().head(10)
plt.figure(figsize=(10, 5))
sns.barplot(x=top_artists.values, y=top_artists.index, palette="viridis")
plt.xlabel("Number of Songs")
plt.ylabel("Artist")
plt.title("Top 10 Artists with Most Songs in the Chart")
plt.show()

# Most Popular Songs (Based on Popularity Score)**
top_songs_popularity = df.nlargest(10, "Popularity")[["Track Name", "Popularity"]]
plt.figure(figsize=(12, 6))
sns.barplot(x="Popularity", y="Track Name", data=top_songs_popularity, palette="coolwarm")
plt.xlabel("Popularity Score")
plt.ylabel("Track Name")
plt.title("Top 10 Most Popular Songs")
plt.show()

#  Most Streamed Songs**
top_songs_streams = df.nlargest(10, "Streams")[["Track Name", "Streams"]]
plt.figure(figsize=(12, 6))
sns.barplot(x="Streams", y="Track Name", data=top_songs_streams, palette="magma")
plt.xlabel("Number of Streams")
plt.ylabel("Track Name")
plt.title("Top 10 Most Streamed Songs")
plt.show()

#  Billboard vs Spotify - Which Platform Has More Songs?**
platform_counts = df["Platform"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(platform_counts, labels=platform_counts.index, autopct="%1.1f%%", colors=["#ff9999", "#66b3ff"], startangle=140)
plt.title("Distribution of Songs Across Platforms")
plt.show()
