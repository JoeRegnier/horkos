
from stat_technique.statisticaltechnique import StatisticalTechnique
from util import math_util
from util import edit_distance_util

class EditDistance_ST(StatisticalTechnique):

    def __init__(self, freqmap, latest_freqmap):
        StatisticalTechnique.__init__(self, freqmap, latest_freqmap)

    def get_name(self):
        return "Edit Distance"

    def process(self):
        if self.freqmap is None or self.latest_freqmap is None:
            return None
        scores = self._process_each_bucket(self.freqmap, self.latest_freqmap)
        self._set_scores(scores)
        return scores

    def _set_scores(self, scores):
        self.scores = scores

    def _process_each_bucket(self, freqmap, latest_freqmap):
        scores = dict()
        for key, bucket in latest_freqmap.items():
            for bucketValue, freq in bucket.items():
                edit_distance = self._min_edit_distance(freqmap[key], bucketValue)
                scores[key + ", " + bucketValue] = self._edit_distance_to_score(edit_distance, len(bucketValue))
        return scores

    def _edit_distance_to_score(self, min_distance, max_length):
        if min_distance >= max_length:
            return 0
        return 1 - (min_distance / max_length)

    def _min_edit_distance(self, freqmap, test_bucket):
        [min_distance, suggestion] = edit_distance_util.edit_distance_comparison(freqmap, test_bucket)
        return min_distance

    def _freq_comparison(self, freqmap, test_bucket):
        return math_util.freqmap_comparison(freqmap, test_bucket)

    def _levenshtein_distance(self, string_one, string_two):
        return edit_distance_util.levenshtein_distance(string_one, string_two)
