import unittest
from stat_technique.unigramprobability_st import UnigramProbability_ST

class UnigramProbabilityST_Test(unittest.TestCase):

    def test_simple(self):
        freqmap = dict()

        inner_freq_map = dict()
        inner_freq_map["10000"] = 300
        inner_freq_map["11000"] = 200
        inner_freq_map["25000"] = 1
        inner_freq_map["30000"] = 1
        freqmap["DJ7R92"] = inner_freq_map

        second_inner_freq_map = dict()
        second_inner_freq_map["10000"] = 2000
        second_inner_freq_map["11000"] = 3000
        second_inner_freq_map["25000"] = 1000
        freqmap["DH6H81"] = second_inner_freq_map

        latest_freqmap = dict()
        third_inner_freq_map = dict()
        third_inner_freq_map["25000"] = 1
        third_inner_freq_map["30000"] = 1
        latest_freqmap["DJ7R92"] = third_inner_freq_map


        unigram_probability_st = UnigramProbability_ST(freqmap, latest_freqmap)
        scores = unigram_probability_st.process()

        self.assertTrue(scores["DJ7R92, 25000"] < scores["DJ7R92, 30000"])




if __name__ == '__main__':
    unittest.main()