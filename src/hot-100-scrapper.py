import billboard
from pymongo import MongoClient

client = MongoClient()
db = client.soul
songs = db.songs
billboard_ranks = db.billboard_ranks

chart = billboard.ChartData('hot-100', date="1988-01-16")

while chart.previousDate:
    chart = billboard.ChartData('hot-100', date=chart.previousDate)
    print(chart.date)
    for rank in range(100):
        song = chart[rank]
        search = { "name": song.title, "artist.name": song.artist }
        lookup = songs.find_one( search )

        if lookup is None:
            song_post = {
                "name": song.title,
                "artist": {
                    "name": song.artist
                }
            }

            song_id = songs.insert_one(song_post).inserted_id

            ranks_post = {
                "date": str(chart.date),
                "rank": rank,
                "song_id": song_id
            }
        else:
            ranks_post = {
                "date": str(chart.date),
                "rank": rank,
                "song_id": lookup["_id"]
            }

        billboard_ranks.insert_one(ranks_post)
