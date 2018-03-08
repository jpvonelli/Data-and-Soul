import pymongo
import numpy as np

class Avg_Std:
    def __init__(self):
        self.feature_list = ["loudness", "duration_ms", "tempo", "key", "instrumentalness", "energy",
                             "acousticness", "speechiness", "time_signature",
                             "danceability", "liveness", "mode", "valence"]
        self.billboard_ranks, self.songs = self.db_setup()
        self.avg_outfile, self.std_outfile, self.total_avg_outfile, self.total_std_outfile = self.outfile_setup(self.feature_list)


    @staticmethod
    def db_setup():
        client = pymongo.MongoClient()
        db = client.soul
        billboard_ranks = db.billboard_ranks
        songs = db.songs

        return billboard_ranks, songs

    @staticmethod
    def outfile_setup(features):
        avg_outfile = open('avg_results.csv', 'w')
        std_outfile = open('std_results.csv', 'w')
        total_avg_outfile = open('avg_results_total.csv', 'w')
        total_std_outfile = open('std_results.csv', 'w')

        avg_outfile.write("Date, ")
        std_outfile.write("Date, ")

        for i in range(len(features)):
            if i == len(features) - 1:
                avg_outfile.write(features[i] + '\n')
                std_outfile.write(features[i] + '\n')
                total_avg_outfile.write(features[i] + '\n')
                total_std_outfile.write(features[i] + '\n')

            else:
                avg_outfile.write(features[i] + ', ')
                std_outfile.write(features[i] + ', ')
                total_avg_outfile.write(features[i] + ', ')
                total_std_outfile.write(features[i] + ', ')

        return avg_outfile, std_outfile, total_avg_outfile, total_std_outfile

    def outfile_close(self):
        self.avg_outfile.close()
        self.std_outfile.close()
        self.total_avg_outfile.close()
        self.total_std_outfile.close()

    def compute_avg_std_data(self):
        current_date = "1958-08-04"
        rank_list = []
        song_id_list = []
        avg_dict = {}
        std_dict = {}
        total_avg_dict = {}
        total_std_dict = {}

        for billboard_document in self.billboard_ranks.find(no_cursor_timeout=True).sort(
                [["date", pymongo.ASCENDING], ["rank", pymongo.ASCENDING]]):
            bill_rank = billboard_document['rank']
            bill_date = billboard_document['date']
            song_id = billboard_document['song_id']

            if current_date != bill_date:
                feature_dict = self.compute_avg_std_for_date(song_id_list)
                avg_dict = self.get_avg(feature_dict)
                std_dict = self.get_std(feature_dict)

                for key in total_avg_dict.keys():
                    print(total_avg_dict[key])
                    total_avg_dict[key].append(avg_dict[key])

                for key in total_std_dict.keys():
                    total_std_dict[key].append(std_dict[key])

                self.write_to_avg_outfile(avg_dict, current_date)
                self.write_to_std_outfile(std_dict, current_date)

                print(current_date)
                rank_list = []
                song_id_list = []
                current_date = bill_date


            song_id_list.append(song_id)

        feature_dict = self.compute_avg_std_for_date(song_id_list)
        avg_dict = self.get_avg(feature_dict)
        std_dict = self.get_std(feature_dict)

        for key in avg_dict.keys():
            total_avg_dict[key].append(avg_dict[key])

        for key in std_dict.keys():
            total_std_dict[key].append(std_dict[key])

        self.write_to_avg_outfile(avg_dict)
        self.write_to_std_outfile(std_dict)
        self.write_to_total_avg_outfile(total_avg_dict)
        self.write_to_total_std_outfile(total_std_dict)

        return

    def compute_avg_std_for_date(self, song_ids):
        feat_dict = {}
        feat_avg_dict = {}
        for feature in self.feature_list:
            feat_dict[feature] = []
            feat_avg_dict[feature] = []

        for key in feat_avg_dict:
            #for item in feat_avg_dict[key]:
            feat_avg = self.compute_feat_avg(song_ids, key)
            feat_avg_dict[key].append(feat_avg)

        for song_id in song_ids:
            song_lookup = self.songs.find_one({"_id": song_id, "spotify_id": {"$exists": True}})
            if song_lookup is not None:
                for feature in self.feature_list:
                    feat_metric = song_lookup["audio_features"][feature]
                    feat_dict[feature].append(feat_metric)
            else:
                for feature in self.feature_list:
                    feat_dict[feature].append(feat_avg_dict[feature][0])

        return feat_dict

    def compute_feat_avg(self, id_list, feature):
        songs_with_features = 0
        average = 0
        for song_id in id_list:
            song_lookup = self.songs.find_one(
                {"_id": song_id, "audio_features." + feature: {"$exists": True}})
            if song_lookup is not None:
                average += song_lookup["audio_features"][feature]
                songs_with_features += 1

        return average / songs_with_features


    def get_avg(self, feat_dict):
        avg_dict = {}
        for key in feat_dict.keys():
            avg_dict[key] = np.mean(feat_dict[key])

        return avg_dict

    def get_std(self, feat_dict):
        std_dict = {}
        for key in feat_dict.keys():
            std_dict[key] = np.std(feat_dict[key])

        return std_dict

    def write_to_avg_outfile(self, avg_dict, current_date):
        total = len(avg_dict.keys())
        count = 0

        self.avg_outfile.write(str(current_date) + ", ")

        for key in avg_dict.keys():
            count += 1
            self.avg_outfile.write(str(avg_dict[key]))
            if count != total:
                self.avg_outfile.write(", ")

        self.avg_outfile.write('\n')

        return

    def write_to_std_outfile(self, std_dict, current_date):
        total = len(std_dict.keys())
        count = 0

        self.std_outfile.write(str(current_date) + ", ")

        for key in std_dict.keys():
            count += 1
            self.std_outfile.write(str(std_dict[key]))
            if count != total:
                self.std_outfile.write(", ")

        self.std_outfile.write('\n')

        return

    def write_to_total_avg_outfile(self, total_avg_dict):
        total = len(total_avg_dict.keys())
        count = 0
        for key in total_avg_dict.keys():
            count += 1
            self.total_avg_outfile.write(str(total_avg_dict[key]))
            if count != total:
                self.total_avg_outfile.write(", ")
        return

    def write_to_total_std_outfile(self, total_std_dict):
        total = len(total_std_dict.keys())
        count = 0
        for key in total_std_dict.keys():
            count += 1
            self.total_avg_outfile.write(str(total_std_dict[key]))
            if count != total:
                self.total_avg_outfile.write(", ")
        return

def run():
    avg_std = Avg_Std()
    avg_std.compute_avg_std_data()
    avg_std.outfile_close()
    return

if __name__ == "__main__":
    run()
