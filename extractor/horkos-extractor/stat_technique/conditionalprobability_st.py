
from stat_technique.statisticaltechnique import StatisticalTechnique
from util import math_util

class ConditionalProbability_ST(StatisticalTechnique):

    def __init__(self, freqmap, latest_freqmap):
        self.scores = dict()
        StatisticalTechnique.__init__(self, freqmap, latest_freqmap)

    def get_name(self):
        return "Conditional Probability"

    def process(self):
        if self.freqmap is None or self.latest_freqmap is None:
            return None
        probabilities = self._process_bucket_probabilities(self.freqmap)

        scores = self._calculate_all_scores(probabilities, self.latest_freqmap)
        self._set_scores(scores)
        return scores

    def _set_scores(self, scores):
        self.scores = scores

    def _calculate_all_scores(self, probabilities, latest_freqmap):
        scores = dict()
        for key, bucket in latest_freqmap.items():
            for bucketValue, _ in bucket.items():
                scores[key+", "+bucketValue] = self._calculate_score(list(probabilities.values()), probabilities[key+", "+bucketValue])
        return scores

    def _calculate_score(self, probabilities, test_value):
        deviation_from_mean = math_util.deviation_from_mean(probabilities, test_value)
        #Only want to measure scores that occur less than average
        if deviation_from_mean > 0:
            score = 0
        else:
            score = 1 - math_util.z_score_to_cheb_values(deviation_from_mean)
        return score


    def _process_bucket_probabilities(self, freqmap):
        probabilities = dict()
        for key, bucket in freqmap.items():
            total_count = self._get_count(freqmap[key])
            for bucketValue, freq in bucket.items():
                probabilities[key + ", " + bucketValue] = freqmap[key].get(bucketValue) / total_count
        return probabilities

    def _get_count(self, freqmap):
        total_count = 0
        for key, value in freqmap.items():
            total_count = total_count + int(value)
        return total_count

    def _freq_comparison(self, freqmap, testBucket):
        return math_util.freqmap_comparison(freqmap, testBucket)