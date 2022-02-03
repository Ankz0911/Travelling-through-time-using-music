# imports
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Constants
spotify_id = "your_spotify_id"
spotify_secret = "your_spotify_secret_key"
spotify_uri = "http://example.com"
spotify_scope = "playlist-modify-private"

# code to get list of top 100 from billboard on a set date
URL = "https://www.billboard.com/charts/hot-100/"
user_input = input("Enter a date in YYYY-MM-DD format\n")

year = user_input.split("-")[0]
final_url = f"{URL}{user_input}/"

billboard_page = requests.get(final_url)
soup = BeautifulSoup(billboard_page.text, "html.parser")
headings = soup.find_all(name="h3", id="title-of-a-story")
songs_list = [song.getText() for song in headings][6::4][:100]
songs_list = [song.split("\n")[1] for song in songs_list]

# code for spotipy authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_id,
                                               client_secret=spotify_secret,
                                               redirect_uri=spotify_uri,
                                               scope=spotify_scope))
details = sp.current_user()
user_id = details["id"]

# code for spotipy work

# 1. creating new playlist

playlist_name = user_input + " " + "Billboard 100"
response = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
playlist_id = response["id"]


# 2. searching and adding songs

songs_spotify_list = []
for song in songs_list:
    try:
        final_name = song + " " + year
        to_be_added = sp.search(q=final_name, type="track")
        to_be_added = to_be_added["tracks"]["items"][0]["uri"]
        songs_spotify_list.append(to_be_added)
        print(to_be_added)
    except IndexError:
        pass

response2 = sp.playlist_add_items(playlist_id=playlist_id, items=songs_spotify_list)
print(response2)
