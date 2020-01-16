from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.
class Query(models.Model):
    queryName = models.CharField(max_length=200)
    querySql = models.CharField(max_length=10000)
    mostRecentRevision = models.IntegerField(default=-1)
    auto_update_revision = models.BooleanField(default=True)
    trailingRevisionNumber = models.IntegerField(default=-1)
    auto_update_trailing_revision = models.BooleanField(default=True)
    key_length = models.IntegerField(default=-1)
    scoreThreshold = models.FloatField(default=0)
    suggestion = models.BooleanField(default=True)
    database_server = models.CharField(max_length=2000, default="")
    database = models.CharField(max_length=2000, default="")
    server_type = models.CharField(max_length=2000, default="", choices=[("mysql", "MySQL"), ("mssql", "MSSQL")])
    context_query = models.CharField(max_length=10000, default="")
    use_neural_network = models.BooleanField(default=False)
    most_recent_run_time = models.FloatField(default=0)
    avg_run_time = models.FloatField(default=0)
    num_recorded_runs = models.IntegerField(default=0)

    def __str__(self):
        return self.database_server + ": " + self.queryName

class StatTechnique(models.Model):
    statTechnique = models.CharField(max_length=100)
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.statTechnique

class StaticWeight(models.Model):
    queryID = models.ForeignKey(Query, on_delete=models.CASCADE)
    statTechnique = models.ForeignKey(StatTechnique, on_delete=models.CASCADE)
    weight = models.FloatField(default=0)
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return str(self.queryID) + " " + str(self.statTechnique) + ": " + str(self.weight)

class FreqMapEntry(models.Model):
    queryID = models.ForeignKey(Query, on_delete=models.CASCADE)
    tupleKey = models.CharField(max_length=2000)
    tupleBucket = models.CharField(max_length=2000)
    tupleValue = models.IntegerField(default=0)

    def __str__(self):
        return self.key

class Issue(models.Model):
    queryID = models.ForeignKey(Query, on_delete=models.CASCADE)
    queryKey = models.CharField(max_length=2000)
    queryValue = models.CharField(max_length=2000)
    overall_score = models.FloatField(default=0)
    explanation = models.CharField(default="", max_length=200)
    suggestion = models.CharField(max_length=2000)
    status = models.CharField(max_length=100, default="New")
    date_opened = models.DateTimeField(default=timezone.now)
    context = models.CharField(max_length=2000)
    indexes = [
        models.Index(fields=['id',]),
        models.Index(fields=['queryID_id',]),
    ]

    class Meta:
        unique_together = ('queryID', 'queryValue',)

class Score(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    statTechnique = models.ForeignKey(StatTechnique, on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    def __str__(self):
        return str(self.statTechnique) + ": " + str(self.weight)
