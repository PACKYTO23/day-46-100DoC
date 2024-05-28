from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

CLIENT_ID = "41db77668dc64df186317025244622c2"
CLIENT_SECRET = "900cb407be0747ddb4167e8a0d3cc219"
REDIRECT_URI = "https://example.com/"
BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

date_selection = input("What year do you want to travel to? Type the date in this format YYYY-MM-DD:\n")
top_100_date = f"{BILLBOARD_URL}{date_selection}/"

response = requests.get(top_100_date)
b_100_webpage = response.text
soup = BeautifulSoup(b_100_webpage, "html.parser")
song_names = soup.select("li ul li h3")
song_titles_list = [song.getText().strip() for song in song_names]
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="FranciscoGP",
    )
)
user_id = sp.current_user()["id"]
song_uris = []
year = date_selection.split("-")[0]

for song in song_titles_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date_selection} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
