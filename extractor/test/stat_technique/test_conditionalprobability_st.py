import unittest
from stat_technique.conditionalprobability_st import ConditionalProbability_ST

class ConditionalProbability_ST_test(unittest.TestCase):

    def test_simple(self):
        freqmap = dict()

        inner_freq_map = dict()
        inner_freq_map["10000"] = 300
        inner_freq_map["11000"] = 200
        inner_freq_map["25000"] = 1
        freqmap["DJ7R92"] = inner_freq_map

        second_inner_freq_map = dict()
        second_inner_freq_map["20000"] = 2000
        second_inner_freq_map["21000"] = 3000
        second_inner_freq_map["45000"] = 1
        freqmap["DH6H81"] = second_inner_freq_map

        latest_freqmap = dict()
        third_inner_freq_map = dict()
        third_inner_freq_map["25000"] = 1
        third_inner_freq_map["11000"] = 1
        latest_freqmap["DJ7R92"] = third_inner_freq_map

        fourth_inner_freq_map = dict()
        fourth_inner_freq_map["45000"] = 1
        fourth_inner_freq_map["21000"] = 1
        latest_freqmap["DH6H81"] = fourth_inner_freq_map

        conditional_prob = ConditionalProbability_ST(freqmap, latest_freqmap)
        scores = conditional_prob.process()

        self.assertTrue(scores["DJ7R92, 11000"] < scores["DJ7R92, 25000"])
        self.assertTrue(scores["DH6H81, 21000"] < scores["DH6H81, 45000"])

if __name__ == '__main__':
    unittest.main()
