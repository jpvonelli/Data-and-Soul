import pymongo

client = pymongo.MongoClient()
db = client.soul
billboard_ranks = db.billboard_ranks

def compute_longevity():
    prev_hash = {}
    current_hash = {}
    current_date = "1958-08-04"

    for document in billboard_ranks.find().sort('_id', pymongo.DESCENDING):
        document_id = document["_id"]
        date = document["date"]
        song_id = document["song_id"]

        if current_date != date:
            update_documents(current_hash, document_id)
            prev_hash = current_hash
            current_hash = {}

        else:
            if song_id in prev_hash.keys():
                current_hash[song_id] = [document_id, prev_hash['song_id'][1] + 1]
            else:
                current_hash[song_id] = [document_id, 1]

    return

def update_documents(current_dict, doc_id, doc_song_id):
    billboard_ranks.update({
        "_id": doc_id
    },
        {
            "$set": {
                "longevity": current_dict[doc_song_id][1]
            }
        }
    )

compute_longevity()

