from scipy import stats
from itertools import combinations
import csv

class Pearson_Corr:
    def __init__(self):
        self.feature_list = ["loudness", "duration_ms", "tempo", "key", "instrumentalness", "energy",
                             "acousticness", "speechiness", "time_signature",
                             "danceability", "liveness", "mode", "valence"]

        self.combos = self.__create_combinations(self.feature_list)
        self.corr_outfile, self.writer = self.__outfile_setup(self.combos)

    @staticmethod
    def __outfile_setup(combinations):
        corr_outfile = open('corr_results.csv', 'w')
        writer = csv.DictWriter(corr_outfile, fieldnames=combinations)
        writer.writeheader()
        return corr_outfile, writer

    @staticmethod
    def __create_combinations(features):
        return list(combinations(features, 2))

    def outfile_close(self):
        self.corr_outfile.close()

    def __read_from_sampling_file(self, feature):
        infile = open('sampling_results_' + feature + '.csv', 'r')
        reader = csv.DictReader(infile)
        data = []

        for metric in reader:
            data.append(float(metric[feature]))

        return data

    def __write_to_file(self, metric):
        self.corr_outfile.write(metric)

    def run_correlation(self):
        total = len(self.combos) - 1
        count = 0
        for couple in self.combos:
            data_set1 = self.__read_from_sampling_file(couple[0])
            data_set2 = self.__read_from_sampling_file(couple[1])

            result = stats.pearsonr(data_set1, data_set2)
            self.corr_outfile.write(str(result))

            if count != total:
                self.corr_outfile.write(', ')

        self.corr_outfile.write('\n')

        return

def run():
    pearson = Pearson_Corr()
    pearson.run_correlation()
    pearson.outfile_close()


if __name__ == "__main__":
    run()