import pymongo
import random
import csv

class Sampler:
    def __init__(self, spot_feat, rank_range=100, sample_size=100, alpha=0.5):
        #self.spot_feat = [feature for feature in spot_feat]
        self.spot_feat = spot_feat
        self.rank_range = rank_range
        self.sample_size = sample_size
        self.alpha = alpha

        self.client, self.db, self.billboard_ranks, self.songs = self.db_setup()
        self.probability_results, self.sampling_results = self.outfile_setup(self.spot_feat)

    @staticmethod
    def db_setup():
        client = pymongo.MongoClient()
        db = client.soul
        billboard_ranks = db.billboard_ranks
        songs = db.songs

        return client, db, billboard_ranks, songs

    @staticmethod
    def outfile_setup(feature):
        sampling_outfile = open('sampling_results.csv', 'w')
        probability_outfile = open('probability_results.txt', 'w')

        sampling_outfile.write("Date," + feature + '\n')

        return probability_outfile, sampling_outfile

    def outfile_close(self):
        self.probability_results.close()
        self.sampling_results.close()


    def sample_data(self):
        current_date = "1958-08-04"
        probability_list = []
        rank_list = []
        longevity_list = []
        song_id_list = []

        for billboard_document in self.billboard_ranks.find().sort([["date", pymongo.ASCENDING], ["rank", pymongo.ASCENDING]]):
            bill_rank = billboard_document['rank']
            bill_date = billboard_document['date']
            song_id = billboard_document['song_id']
            bill_longevity = billboard_document['longevity']

            if current_date != bill_date:
                print(current_date)
                longevity_sum = sum(longevity_list)
                rank_sum = sum(rank_list)

                if len(longevity_list) != len(rank_list):
                    raise Exception

                probability_list = [self.compute_probability(rank_list[i], rank_sum, longevity_list[i],
                                                             longevity_sum, self.alpha) for i in range(100)]

                self.write_to_probability_outfile(probability_list, current_date)

                weighted_average = self.get_weighted_sample(probability_list, song_id_list)
                self.write_to_sampling_outfile(current_date, weighted_average)
                rank_list = []
                longevity_list = []
                song_id_list = []
                current_date = bill_date

            # only computing numerators
            rank_list.append(self.rank_range + 1 - bill_rank)
            longevity_list.append(bill_longevity)
            song_id_list.append(song_id)

            #song_document = self.songs.find_one({"song_id": billboard_document["song_id"]})

    def get_weighted_sample(self, prob, id_list):
        feat_avg, total_songs_with_features = self.compute_feat_avg(id_list)
        weighted_average = 0

        for i in range(self.sample_size):
            rank = self.get_rank_sample(prob)

            song_lookup = self.songs.find_one({"_id": id_list[rank], "audio_features." + self.spot_feat: {"$exists": True}})
            if song_lookup is None:
                weighted_average += feat_avg
            else:
                weighted_average += song_lookup["audio_features"][self.spot_feat]


        return  weighted_average / self.sample_size

    def compute_feat_avg(self, id_list):
        songs_with_features = 0
        average = 0
        for song_id in id_list:
            song_lookup = self.songs.find_one({ "_id": song_id, "audio_features." + self.spot_feat: {"$exists": True}})
            if song_lookup is not None:
                average += song_lookup["audio_features"][self.spot_feat]
                songs_with_features += 1

        return average / songs_with_features, songs_with_features

    def get_rank_sample(self, prob):
        r = random.uniform(min(prob), sum(prob))
        selected = []

        for i in range(len(prob)):
            r = r - prob[i]
            if r <= 0:
                return i

    def compute_probability(self, rank, rank_sum, longevity, longevity_sum, alpha):
        return alpha * (rank / rank_sum) + (1 - alpha) * (longevity / longevity_sum)

    def write_to_sampling_outfile(self, date, average):
        self.sampling_results.write(str(date) + "," + str(average) + '\n')
        return

    def write_to_probability_outfile(self, prob_list, date):
        self.probability_results.write("Date:" + date + "\n")
        for i,prob in enumerate(prob_list):
            self.probability_results.write(str(i) + ": " + str(prob) + "\n")

        return

def run():
    sample = Sampler("danceability")
    sample.sample_data()
    sample.outfile_close()

if __name__ == "__main__":
    run()