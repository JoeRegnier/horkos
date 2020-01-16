
from functools import *
from util import math_util


def edit_distance_comparison(freqmap, test_bucket):
    min_distance = len(test_bucket)
    base_freq = math_util.freqmap_comparison(freqmap, test_bucket)
    highest_freq = base_freq
    suggestion = ""
    for key, bucket in freqmap.items():
        cur_distance = levenshtein_distance(str(key), str(test_bucket))
        cur_freq = math_util.freqmap_comparison(freqmap, key)
        if key != test_bucket:
            if cur_freq > base_freq:
                    if cur_distance == min_distance and highest_freq < cur_freq:
                        min_distance = cur_distance
                        highest_freq = cur_freq
                        suggestion = key
                    elif cur_distance < min_distance:
                        min_distance = cur_distance
                        highest_freq = cur_freq
                        suggestion = key
    return [min_distance, suggestion]

def levenshtein_distance(string_one, string_two):
    if len(string_one) > len(string_two):
        string_one, string_two = string_two, string_one

    distances = range(len(string_one) + 1)
    for i2, c2 in enumerate(string_two):
        distances_ = [i2+1]
        for i1, c1 in enumerate(string_one):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]