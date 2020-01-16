
class statsQuery:
    def __init__(self, queryName):
        self.queryName = queryName

    def setQueryID(self, queryID):
        self.queryID = queryID

    def getQueryID(self):
        return self.queryID

    def getQueryName(self):
        return self.queryName

    def setSqlQuery(self, sqlQuery):
        self.sqlQuery = sqlQuery

    def getSqlQuery(self):
        return self.sqlQuery

    def setMostRecentRevision(self, mostRecentRevision):
        self.mostRecentRevision = mostRecentRevision

    def getMostRecentRevision(self):
        return self.mostRecentRevision

    def setTrailingRevisionNumber(self, trailingRevisionNumber):
        self.trailingRevisionNumber = trailingRevisionNumber

    def getTrailingRevisionNumber(self):
        return self.trailingRevisionNumber

    def setKeyLength(self, keyLength):
        self.keyLength = keyLength

    def getKeyLength(self):
        return self.keyLength

    def setTargetConnection(self, targetConn):
        self.targetConn = targetConn

    def getTargetConnection(self):
        return self.targetConn

    def setScoreThreshold(self, Score):
        self.Score = Score

    def getScoreThreshold(self):
        return self.Score

    def setDatabaseName(self, databaseName):
        self.databaseName = databaseName

    def getDatabaseName(self):
        return self.databaseName

    def get_static_weights(self):
        return self.static_weights

    def set_static_weights(self, static_weights):
        self.static_weights = static_weights

    def __str__(self):
        return self.queryName