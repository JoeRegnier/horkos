# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class CommonIssue(models.Model):
    queryid = models.ForeignKey('CommonQuery', models.DO_NOTHING, db_column='queryID_id')
    status = models.CharField(max_length=100)
    queryvalue = models.CharField(db_column='queryValue', max_length=2000)
    querykey = models.CharField(db_column='queryKey', max_length=2000)
    suggestion = models.CharField(max_length=2000)
    overall_score = models.FloatField()
    explanation = models.CharField(max_length=200)
    date_opened = models.DateTimeField()
    context = models.CharField(max_length=2000)

    class Meta:
        managed = False
        db_table = 'common_issue'
        unique_together = ('queryid','queryvalue',)


class CommonQuery(models.Model):
    queryname = models.CharField(db_column='queryName', max_length=200)
    querysql = models.CharField(db_column='querySql', max_length=10000)
    key_length = models.IntegerField()
    mostrecentrevision = models.IntegerField(db_column='mostRecentRevision')
    trailingrevisionnumber = models.IntegerField(db_column='trailingRevisionNumber')
    auto_update_revision = models.BooleanField(db_column='auto_update_revision')
    trailingrevisionnumber = models.IntegerField(db_column='trailingRevisionNumber')
    auto_update_trailing_revision = models.BooleanField(db_column='auto_update_trailing_revision')
    database_server = models.CharField(db_column='database_server', max_length=2000)
    database = models.CharField(db_column='database', max_length=2000)
    server_type = models.CharField(db_column='server_type', max_length=2000)
    scorethreshold = models.FloatField(db_column='scoreThreshold')
    suggestion = models.IntegerField()
    context_query = models.CharField(db_column='context_query')
    use_neural_network = models.BooleanField(db_column='use_neural_network')
    most_recent_run_time = models.FloatField(db_column='most_recent_run_time')
    avg_run_time = models.FloatField(db_column='avg_run_time')
    num_recorded_runs = models.IntegerField(db_column='num_recorded_runs')

    class Meta:
        managed = False
        db_table = 'common_query'

class CommonStaticweight(models.Model):
    stattechnique = models.ForeignKey('CommonStattechnique', models.DO_NOTHING, db_column='statTechnique_id')
    weight = models.FloatField()
    queryid = models.ForeignKey(CommonQuery, models.DO_NOTHING, db_column='queryID_id')
    enabled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'common_staticweight'


class CommonStattechnique(models.Model):
    stattechnique = models.CharField(db_column='statTechnique', max_length=100)
    description = models.CharField(db_column='description', max_length=250)

    class Meta:
        managed = False
        db_table = 'common_stattechnique'

class CommonScore(models.Model):
    score = models.FloatField()
    issue = models.ForeignKey(CommonIssue, models.DO_NOTHING)
    stattechnique = models.ForeignKey('CommonStattechnique', models.DO_NOTHING, db_column='statTechnique_id')

    class Meta:
        managed = False
        db_table = 'common_score'