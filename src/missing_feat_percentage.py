import pymongo

client = pymongo.MongoClient()
db = client.soul
billboard_ranks = db.billboard_ranks
songs = db.songs

outfile = open('missing_feat_percentage.txt', 'w')
current_date = "1958-08-04"
missing_spotify_feat_count = 0

for billboard_document in billboard_ranks.find(no_cursor_timeout=True).sort(
                [["date", pymongo.ASCENDING], ["rank", pymongo.ASCENDING]]):
    #bill_rank = billboard_document['rank']
    bill_date = billboard_document['date']
    song_id = billboard_document['song_id']

    song_lookup = songs.find_one({"_id": song_id, "spotify_id": {'$exists': True}})

    if current_date != bill_date:
        if missing_spotify_feat_count > 5:
            outfile.write(str(current_date) + ", " + str(missing_spotify_feat_count))
        missing_spotify_feat_count = 0
        current_date = 0

    if song_lookup is None:
        missing_spotify_feat_count += 1


