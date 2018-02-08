import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pymongo import MongoClient
import yaml

client = MongoClient()
db = client.soul
songs = db.songs

id_outfile = open("spotify_id_missing.txt", "w")
credentials = yaml.load(open("credentials.yml", "r"))

# Remember to remove credentials!
client_credentials_manager = SpotifyClientCredentials(credentials["spotify"]["client"], credentials["spotify"]["secret"])
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
        song_artist = song_artist.split("Featuring", 1)[0].strip()

    # grabs spotify id
    try:
        search_results = sp.search(q='artist:{} track:{}'.format(song_artist, song_name), type='track')
    except Exception as ex:
        id_outfile.write(song_artist + ", " + song_name + ": " + "Spotify track returns 404 error" + "\n")
        print(song_artist + ", " + song_name + ": " + "Spotify track returns 404 error" + "\n")
        song_count+=1
        continue

    try:
        spotify_id = search_results["tracks"]["items"][0]["id"]
    except Exception as ex:
        id_outfile.write(song_artist + ", " + song_name + ": " + "Spotify track_id not found" + "\n")
        print(song_artist + ", " + song_name + ": " + "Spotify track_id not found")
        song_count+=1
        continue

    # Grabs audio analysis
    #audio_analysis = sp.audio_analysis(spotify_id)

    try:
        audio_features = sp.audio_features(spotify_id)
    except Exception as ex:
        id_outfile.write(song_artist + ", " + song_name + ": " + "Spotify audio features result not found" + "\n")
        print(song_artist + ", " + song_name + ": " + "Spotify audio features result not found")
        song_count += 1
        continue

    # tries to grab audio features for mongo db post
    try:
        danceability = audio_features[0]["danceability"]
        energy = audio_features[0]["energy"]
        key = audio_features[0]["key"]
        loudness = audio_features[0]["loudness"]
        mode = audio_features[0]["mode"]
        speechiness = audio_features[0]["speechiness"]
        acousticness = audio_features[0]["acousticness"]
        instrumentalness = audio_features[0]["instrumentalness"]
        liveness = audio_features[0]["liveness"]
        valence = audio_features[0]["valence"]
        tempo = audio_features[0]["tempo"]
        duration_ms = audio_features[0]["duration_ms"]
        time_signature = audio_features[0]["time_signature"]
    except Exception as ex:
        id_outfile.write(song_artist + ", " + song_name + ": " + "Spotify audio features are incomplete" + "\n")
        print(song_artist + ", " + song_name + ": " + "Spotify audio features are incomplete" + "\n")
        song_count += 1
        continue

    # updates document with audio_features
    songs.update({
        "_id": song_db_id
        },
        {
            "$set":{
            "spotify_id": spotify_id,
            "audio_features":{
                    "danceability": danceability,
                    "energy": energy,
                    "key": key,
                    "loudness": loudness,
                    "mode": mode,
                    "speechiness": speechiness,
                    "acousticness": acousticness,
                    "instrumentalness": instrumentalness,
                    "liveness": liveness,
                    "valence": valence,
                    "tempo": tempo,
                    "duration_ms": duration_ms,
                    "time_signature": time_signature
                }
            }
        }
    )

    song_count += 1

id_outfile.close()
