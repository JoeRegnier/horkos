

__all__ = ('')

"""
Parent class to keep all statistical queries uniform
"""
class StatisticalTechnique():

    def __init__(self, freqmap, latest_freqmap):
        self.freqmap = freqmap
        self.latest_freqmap = latest_freqmap
        self.scores = dict()

    def get_name(self):
        pass

    def process(self):
        pass

    def get_scores(self):
        return self.scores

    def get_freqmap(self):
        return self.freqmap

    def get_latest_freqmap(self):
        return self.latest_freqmap