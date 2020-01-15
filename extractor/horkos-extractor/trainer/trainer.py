from manager.statquery_manager import StatQueryManager
from manager import database_connection_manager
from data.models import CommonIssue, CommonQuery

class Trainer():

    def __init__(self):
        pass

    def train_thresholds(self):
        query_manager = StatQueryManager()
        stat_queries = CommonQuery.objects.all()
        for stat_query in stat_queries:
            issues = CommonIssue.objects.filter(queryid=stat_query)
            ignored_sum = 0.0
            verified_sum = 0.0
            ignored_count = 0
            verified_count = 0
            for issue in issues:
                if issue.status=="Ignored":
                    ignored_sum += issue.overall_score
                    ignored_count += 1
                if issue.status=="Verified":
                    verified_sum += issue.overall_score
                    verified_count += 1
            if ignored_count != 0 and verified_count != 0:
                ignored_avg = ignored_sum / ignored_count
                verified_avg = verified_sum / verified_count
                #Skew towards false-positives
                threshold = (ignored_avg + verified_avg) / 2.1
                stat_query.scorethreshold = threshold
                stat_query.save()

