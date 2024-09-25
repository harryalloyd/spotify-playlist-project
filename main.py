from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import load_dotenv
import os
# Load environment variables from the .env file
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
USERNAME = os.getenv("USERNAME")


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")

# this gets the song names by themselves in a list without any random clutter involved with scraping.
song_names = [song.getText().strip() for song in song_names_spans]

# Spotify Authentication. API docs
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8888/callback",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)

# grabs the username, this can also just be found in my profile. API docs
user_id = sp.current_user()["id"]

# Searching Spotify for songs by title
song_uris = []

# I think it's important to grab the specified year because there might be more than one song with the same name
year = date.split("-")[0]

# iterating over the 100 songs
for song in song_names:
    # this searches for the song in the specified year. API docs
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        print(result)
        # use a JSON Viewer to find the path to the "uri." First print "result" then copy/paste it into the viewer.
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        # If the song wasn't found in Spotify
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify. API docs
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# Adding songs found into the new playlist. API docs
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
