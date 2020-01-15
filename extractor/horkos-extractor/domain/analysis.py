

class Analysis:
    def __init__(self):
        self.status = "New"
        self.minEditDistance = 0
        self.deviationFromMean = 0

    def setQueryKey(self, queryKey):
        self.queryKey = queryKey

    def getQueryKey(self):
        return self.queryKey

    def setQueryValue(self, queryValue):
        self.queryValue = queryValue

    def getQueryValue(self):
        return self.queryValue

    def setQueryID(self, queryID):
        self.queryID = queryID

    def getQueryID(self):
        return self.queryID

    def setScore(self, score):
        self.score = score

    def getScore(self):
        return self.score

    def setExplanation(self, explanation):
        self.explanation = explanation

    def getExplanation(self):
        return self.explanation

    def setProbability(self, probability):
        self.probability = probability

    def getProbability(self):
        return self.probability

    def setSuggestion(self, suggestion):
        self.suggestion = suggestion

    def getSuggestion(self):
        return self.suggestion

    def setMinEditDistance(self, minEditDistance):
        self.minEditDistance = minEditDistance

    def getMinEditDistance(self):
        return self.minEditDistance

    def setDeviationFromMean(self, deviationFromMean):
        self.deviationFromMean = deviationFromMean

    def getDeviationFromMean(self):
        return self.deviationFromMean

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return self.status