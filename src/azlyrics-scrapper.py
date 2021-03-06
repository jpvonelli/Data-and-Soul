import re
import urllib.request
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

def get_lyrics(artist, song_title):
    artist = artist.lower()
    song_title = song_title.lower()
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song_title = re.sub('[^A-Za-z0-9]+', "", song_title)
    if artist.startswith("the"):  # removes starting "the" from artist name
        artist = artist[3:]
    url = "http://azlyrics.com/lyrics/" + artist + "/" + song_title + ".html"

    try:
        content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics = str(soup)
        # lyrics lies between up_partition and down_partition
        up_partition = '<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->'
        down_partition = '<!-- MxM banner -->'
        lyrics = lyrics.split(up_partition)[1]
        lyrics = lyrics.split(down_partition)[0]
        lyrics = lyrics.replace('<br>', '').replace('</br>', '').replace('</div>', '').replace('<br/>', '').strip()
        return lyrics
    except Exception as e:
        return "Exception occurred \n" + str(e)

lyrics_outfile = open("missing_lyrics.txt", "w")

client = MongoClient()
db = client.soul
songs = db.songs
billboard_ranks = db.billboard_ranks

total_songs = songs.count()
song_count = 0

for song in songs.find():
    song_artist = song['artist']['name']
    song_name = song['name']
    song_id = song['_id']

    print(song_count, song_count, song_name, song_artist)

    if "featuring" in song_artist.lower():
        song_artist = song_artist.split("Featuring", 1)[0].strip()

    try:
        lyrics = get_lyrics(song_artist, song_name)
        lyrics_text = re.sub('<i>.*</i>\n', '', lyrics)
    except Exception as ex:
        lyrics_outfile.write(song_artist + ", " + song_name + ": " + "Lyric information not found")
        print(song_artist + ", " + song_name + ": " + "Lyric information not found")
        song_count += 1
        continue

    songs.update({
        "_id": song_id
        },
        {
            "$set":{
            "lyrics":{
                    "text": lyrics_text
                }
            }
        }
    )


    song_count += 1

lyrics_outfile.close()
