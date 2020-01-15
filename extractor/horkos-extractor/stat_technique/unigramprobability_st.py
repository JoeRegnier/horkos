from stat_technique.statisticaltechnique import StatisticalTechnique
from util import math_util


class UnigramProbability_ST(StatisticalTechnique):

    def __init__(self, freqmap, latest_freqmap):
        StatisticalTechnique.__init__(self, freqmap, latest_freqmap)

    def get_name(self):
        return "Unigram Probability"

    def process(self):
        if self.freqmap is None or self.latest_freqmap is None:
            return None
        unigram_freqmap = self._freqmap_to_unigram_map(self.freqmap)
        unigram_probabilities = self._process_unigram_probabilities(unigram_freqmap)
        scores = self._calculate_all_scores(unigram_probabilities, self.latest_freqmap)
        self._set_scores(scores)
        return scores

    def _set_scores(self, scores):
        self.scores = scores

    def _calculate_all_scores(self, probabilities, latest_freqmap):
        scores = dict()
        for key, bucket in latest_freqmap.items():
            for bucket_value, freq in bucket.items():
                scores[key+", "+bucket_value] = self._calculate_score(list(probabilities.values()), probabilities[bucket_value])
        return scores

    def _calculate_score(self, probabilities, test_value):
        deviation_from_mean = math_util.deviation_from_mean(probabilities, test_value)
        #Only want to measure scores that occur less than average
        if deviation_from_mean > 0:
            score = 0
        else:
            score = 1 - math_util.z_score_to_cheb_values(deviation_from_mean)
        return score

    def _freqmap_to_unigram_map(self, freqmap):
        unigram_freq = dict()
        for key, bucket in freqmap.items():
            for bucket_value, freq in bucket.items():
                if unigram_freq.get(bucket_value) is None:
                    unigram_freq[bucket_value] = freq
                else:
                    unigram_freq[bucket_value] += freq
        return unigram_freq

    def _process_unigram_probabilities(self, unigram_freqmap):
        probabilities = dict()
        for bucket, value in unigram_freqmap.items():
            probabilities[bucket] = self._freq_comparison(unigram_freqmap, bucket)
        return probabilities

    def _freq_comparison(self, freqmap, testBucket):
        return math_util.freqmap_comparison(freqmap, testBucket)