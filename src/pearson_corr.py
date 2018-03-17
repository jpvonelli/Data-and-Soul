from scipy import stats
from itertools import combinations
import csv

class Pearson_Corr:
    def __init__(self, alpha=''):
        self.feature_list = ["loudness", "duration_ms", "tempo", "key", "instrumentalness", "energy",
                             "acousticness", "speechiness", "time_signature",
                             "danceability", "liveness", "mode", "valence"]

        self.alpha = alpha

        self.combos = self.__create_combinations(self.feature_list)
        self.corr_outfile = self.__outfile_setup()

    @staticmethod
    def __outfile_setup():
        corr_outfile = open('corr_results.csv', 'w')
        corr_outfile.write('Combination, ' + 'Pearson Correlation Coefficient, ' + 'P-Value' + '\n')
        return corr_outfile

    @staticmethod
    def __create_combinations(features):
        return list(combinations(features, 2))

    def outfile_close(self):
        self.corr_outfile.close()

    def __read_from_sampling_file(self, feature):
        if self.alpha != '':
            infile = open('sampling_results_' + self.alpha + '_preference_' + feature + 'csv', 'r')
        else:
            infile = open('sampling_results_' + feature + '.csv', 'r')
            
        reader = csv.DictReader(infile)
        data = []

        for metric in reader:
            if metric['Date'] == '1958-08-04':
                continue
            
            data.append(float(metric[feature]))

        return data

    def __write_to_file(self, metric):
        self.corr_outfile.write(metric)

    def run_correlation(self):
        for couple in self.combos:
            data_set1 = self.__read_from_sampling_file(couple[0])
            data_set2 = self.__read_from_sampling_file(couple[1])

            result = stats.pearsonr(data_set1, data_set2)

            if result[0] >= 0.75 or result[0] <= -0.75:
                self.corr_outfile.write(str(couple) + ', ' + str(result[0]) + ', ' + str(result[1]) + '\n')

        return

def run():
    pearson = Pearson_Corr(alpha='rank')
    pearson.run_correlation()
    pearson.outfile_close()


if __name__ == "__main__":
    run()