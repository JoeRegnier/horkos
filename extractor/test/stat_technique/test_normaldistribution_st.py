import unittest
from stat_technique.normaldistribution_st import NormalDistribution_ST

class NormalDistribution_ST_Test(unittest.TestCase):

    def test_simple(self):
        freqmap = dict()

        inner_freq_map = dict()
        inner_freq_map["10000"] = 300
        inner_freq_map["15000"] = 300
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
        third_inner_freq_map["15000"] = 1
        latest_freqmap["DJ7R92"] = third_inner_freq_map

        fourth_inner_freq_map = dict()
        fourth_inner_freq_map["45000"] = 1
        fourth_inner_freq_map["21000"] = 1
        latest_freqmap["DH6H81"] = fourth_inner_freq_map

        normal_distribution = NormalDistribution_ST(freqmap, latest_freqmap)
        scores = normal_distribution.process()

        self.assertTrue(scores["DJ7R92, 25000"] > scores["DJ7R92, 15000"])
        self.assertTrue(scores["DH6H81, 45000"] > scores["DH6H81, 21000"])



