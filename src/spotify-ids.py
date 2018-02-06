import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient

client = MongoClient()
db = client.spotify_ingest
songs = db.songs

analysis_outfile = open("missed_song_analysis.txt", "w")
id_outfile = open("spotify_id_missing.txt", "w")

client_credentials_manager = SpotifyClientCredentials("2b17af7dc451456e9346c2af84ced427", "b02f2db7091b488092f10658edad8993")
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# loops through db to grab each song

total_songs = songs.count()
song_count = 0

for song in songs.find():
    song_artist = song["artist"]['name']
    song_name = song["name"]
    song_db_id = song["_id"]

    print(song_artist, song_name)
    print(str(song_count) + " of " + str(total_songs))

    # Removes featuring from artist names, easier for spotify lookup
    if "featuring" in song_artist.lower():
        song_artist = song_artist.split("Featuring", 1)[0]

    # grabs spotify id
    search_results = sp.search(q='artist:{} track:{}'.format(song_artist, song_name), type='track')

    try:
        spotify_id = search_results["tracks"]["items"][0]["id"]
    except Exception as ex:
        id_outfile.write(song_artist + ", " + song_name + ": " + "Spotify track not found")
        print(song_artist + ", " + song_name + ": " + "Spotify track not found")
        song_count+=1
        continue

    # Grabs audio analysis
    audio_analysis = sp.audio_analysis(spotify_id)
    audio_features = sp.audio_features(spotify_id)

    # updates document with audio_features
    songs.update({
        "_id": song_db_id
        },
        {
            "$set":{
            "audio_features":{
                    "danceability": audio_features[0]["danceability"],
                    "energy": audio_features[0]["energy"],
                    "key": audio_features[0]["key"],
                    "loudness": audio_features[0]["loudness"],
                    "mode": audio_features[0]["mode"],
                    "speechiness": audio_features[0]["speechiness"],
                    "acousticness": audio_features[0]["acousticness"],
                    "instrumentalness": audio_features[0]["instrumentalness"],
                    "liveness": audio_features[0]["liveness"],
                    "valence": audio_features[0]["valence"],
                    "tempo": audio_features[0]["tempo"],
                    "duration_ms": audio_features[0]["duration_ms"],
                    "time_signature": audio_features[0]["time_signature"]
                }
            }
        }
    )

    song_count += 1

analysis_outfile.close()
id_outfile.close()

"""
for song in songs.find()
    get id
    lookup on spotify and get spotify_id and analysis
    add to document
"""
