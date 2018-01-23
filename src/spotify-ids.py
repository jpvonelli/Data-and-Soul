import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient

client = MongoClient()
db = client.billboard.db
tracks = db.tracks

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

search_results = sp.search(q='artist:{} track:{}'.format("Radiohead", "Creep"))
track_id = search_results["tracks"]["items"][2]["id"]

audio_feat = sp.audio_features([track_id])
print(audio_feat)



