import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch credentials from environment
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Define the required Spotify scopes
scopes = "user-read-email"

# Authenticate and fetch user info
try:
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id, 
        client_secret=client_secret, 
        redirect_uri=redirect_uri, 
        scope=scopes,
        show_dialog=False  # Uses cached token if available
    ))

    # Get logged-in user details
    user_info = sp.current_user()
    user_email = user_info.get("email", "Unknown Email")

    print(f"\n✅ Authentication Successful")
    print(f"📧 Logged-in User Email: {user_email}")

except Exception as e:
    print(f"❌ Authentication Failed: {e}")
