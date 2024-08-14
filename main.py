import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
from bs4 import BeautifulSoup
import os


client_ID = "d8870ba3219d4726904b1a5e0b1a2073"
client_secret = "2a401ee3bebb4fc6829e1eb11479f22d"


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=client_ID,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Brandon Vela"
    )
)

user_id = sp.current_user()["id"]



date = input("Please input date YYYY-MM-DD: ")



url = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=url)

top100 = response.text

soup = BeautifulSoup(top100, "html.parser")


titles = soup.select("li ul li h3")

all_titles = [song.getText().strip() for song in titles]

year = date.split("-")[0]
song_uris = []

for song in all_titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)

    except IndexError:
        print(f"{song} doesn't exist on spotify, song has been skipped")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Top 100", public=False)


sp.playlist_add_items(playlist_id=playlist['id'], items=song_uris)

print(playlist["id"])


