import pymysql
from domain.statquery import statsQuery
from data.models import CommonQuery, CommonStaticweight
from django.db import connection

class StatQueryManager():

    def __init__(self):
        self.statsQueries = []

    def get_queries(self):
        connection.connect()
        queries = CommonQuery.objects.all()
        return list(queries)

    def get_static_weights(self, search_query):
        connection.connect()
        static_weights = CommonStaticweight.objects.filter(queryid=search_query)
        return static_weights

    def update_most_recent_revision(self, stat_query, highest_revision):
        connection.connect()
        stat_query.mostrecentrevision = highest_revision
        stat_query.save()

    def update_trailing_revision(self, stat_query, trailing_revision):
        connection.connect()
        stat_query.trailingrevisionnumber = trailing_revision
        stat_query.save()

    def update_run_times(self, stat_query, timing):
        connection.connect()
        stat_query.most_recent_run_time = timing
        stat_query.num_recorded_runs = stat_query.num_recorded_runs + 1
        stat_query.avg_run_time = (timing + (stat_query.avg_run_time * (stat_query.num_recorded_runs - 1))) / stat_query.num_recorded_runs
        stat_query.save()