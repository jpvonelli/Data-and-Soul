import pymongo

client = pymongo.MongoClient()
db = client.spotify_ingest
billboard_ranks = db.billboard_ranks

for document in billboard_ranks.find():
    document_id = document["_id"]
    rank = document["rank"] + 1

    billboard_ranks.update({
        "_id": document_id
        },
        {
            "$set": {
                "rank": rank
            }
        }
    )

