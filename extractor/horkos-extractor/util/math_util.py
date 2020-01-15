from scipy import stats, special

def freqmap_comparison(freqmap, testBucket):
    totalCount = 0
    for key, value in freqmap.items():
        totalCount = totalCount + int(value)
    return freqmap.get(testBucket) / totalCount

def deviation_from_mean(data_set, test_value):
    a = deviation_from_mean_all(data_set)
    return a[data_set.index(test_value)]

def deviation_from_mean_all(data_set):
    return stats.zscore(data_set)

#https://en.wikipedia.org/wiki/Chebyshev%27s_inequality
def z_score_to_cheb_values(z_scores):
    if z_scores > 0:
        return 1
    if z_scores < -1.41:
        return 1 - ((1 - (1/(z_scores**2))))
    else:
        #Aims to create a more consistent line from 0 to 1
        return 1 - (abs(z_scores) / 2.88)


def map_floats(value):
    if value != 'None':
        return float(value)