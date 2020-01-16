from stat_technique.statisticaltechnique import StatisticalTechnique
from util import math_util

class NormalDistribution_ST(StatisticalTechnique):

    def __init__(self, freqmap, latest_freqmap):
        StatisticalTechnique.__init__(self, freqmap, latest_freqmap)

    def get_name(self):
        return "Normal Distribution"

    def process(self):
        if self.freqmap is None or self.latest_freqmap is None:
            return None

        stddevs = self._process_bucket_stddev(self.freqmap, self.latest_freqmap)
        scores = self._calculate_all_scores(stddevs, self.latest_freqmap)
        self._set_scores(scores)
        return scores

    def _set_scores(self, scores):
        self.scores = scores

    def _calculate_all_scores(self, stddevs, latest_freqmap):
        scores = dict()
        for key, bucket in latest_freqmap.items():
            for bucket_value, freq in bucket.items():
                scores[key+", "+bucket_value] = self._calculate_score(stddevs[key+", "+bucket_value])
        return scores

    def _calculate_score(self, deviation_from_mean):
        score = 1 - math_util.z_score_to_cheb_values(-abs(deviation_from_mean))
        return score

    def _process_bucket_stddev(self, freqmap, latest_freqmap):
        stddevs = dict()
        for key, bucket in latest_freqmap.items():
            for bucket_value, freq in bucket.items():
                stddevs[key+", "+bucket_value] = self._stddev_comparison(freqmap[key], bucket_value)
        return stddevs

    def _stddev_comparison(self, freqmap, test_bucket):
        if test_bucket == 'None':
            return 0
        return math_util.deviation_from_mean(list(map(math_util.map_floats, freqmap.keys())), float(test_bucket))
