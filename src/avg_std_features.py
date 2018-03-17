import numpy as np
import csv

class Avg_Std:
    def __init__(self, alpha_preference = ''):
        self.feature_list = ["loudness", "duration_ms", "tempo", "key", "instrumentalness", "energy",
                             "acousticness", "speechiness", "time_signature",
                             "danceability", "liveness", "mode", "valence"]

        self.alpha_preference = alpha_preference

        self.avg_outfile, self.std_outfile = self.__outfile_setup(self.feature_list, self.alpha_preference)

    @staticmethod
    def __outfile_setup(features, alpha):
        alpha_outfile = '_' + alpha
        avg_outfile = open('avg_results' + alpha_outfile + '.csv', 'w')
        std_outfile = open('std_results' + alpha_outfile + '.csv', 'w')

        for i in range(len(features)):
            if i == len(features) - 1:
                avg_outfile.write(features[i] + '\n')
                std_outfile.write(features[i] + '\n')

            else:
                avg_outfile.write(features[i] + ', ')
                std_outfile.write(features[i] + ', ')

        return avg_outfile, std_outfile

    def __outfile_close(self):
        self.avg_outfile.close()
        self.std_outfile.close()

    @staticmethod
    def __setup_infile(feature, alpha):
        if alpha != '':
            return open('sampling_results_' + alpha + '_preference' + '_' + feature + '.csv', 'r')

        return open('sampling_results_' + feature + '.csv', 'r')

    def avg_std(self):
        feat_avg = [self.__compute_avg_from_csv(feature) for feature in self.feature_list]
        feat_std = [self.__compute_std_from_csv(feature) for feature in self.feature_list]

        self.__write_to_avg_outfile(feat_avg)
        self.__write_to_std_outfile(feat_std)
        self.__outfile_close()

        return

    def __compute_avg_from_csv(self, feature):
        feature_infile =  self.__setup_infile(feature, self.alpha_preference)
        reader = csv.DictReader(feature_infile)
        feat_metrics = []

        for item in reader:
            if item['Date'] == '1958-08-04':
                continue
            feat_metrics.append(float(item[feature]))

        return self.__get_avg(feat_metrics)

    def __compute_std_from_csv(self, feature):
        feature_infile = self.__setup_infile(feature, self.alpha_preference)
        reader = csv.DictReader(feature_infile)
        feat_metrics = []

        for item in reader:
            feat_metrics.append(float(item[feature]))

        return self.__get_std(feat_metrics)

    def __write_to_avg_outfile(self, feat_list):
        total = len(feat_list) - 1
        for i in range(len(feat_list)):
            self.avg_outfile.write(str(feat_list[i]))
            if i != total:
                self.avg_outfile.write(', ')

        self.avg_outfile.write('\n')

        return

    def __write_to_std_outfile(self, feat_list):
        total = len(feat_list) - 1
        for i in range(len(feat_list)):
            self.std_outfile.write(str(feat_list[i]))
            if i != total:
                self.std_outfile.write(', ')

        self.std_outfile.write('\n')

        return

    @staticmethod
    def __get_avg(feat_list):
        return np.mean(feat_list)

    @staticmethod
    def __get_std(feat_list):
        return np.std(feat_list)



def run():
    avg_std = Avg_Std('rank')
    avg_std.avg_std()
    return

if __name__ == "__main__":
    run()
