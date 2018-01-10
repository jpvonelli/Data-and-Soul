import billboard
from pymongo import MongoClient
import os

client = MongoClient()
db = client.billboard_db
tracks = db.tracks

chart = billboard.ChartData('hot-100')

while chart.previousDate:
	chart = billboard.ChartData('hot-100', date=chart.previousDate)
	chartDate = chart.date
	print(chartDate)

	for rank in range(100):
		song = chart[rank]
		post = {
			"spotify_id": " ",
			"track": str(song.title),
			"artist": str(song.artist),
			"rank": rank,
			"peak": str(song.peakPos),
			"lastPos": str(song.lastPos),
			"weeks": str(song.weeks),
			"date": chart.date
		}

		insert = tracks.insert_one(post).inserted_id

