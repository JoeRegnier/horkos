import os
import argparse
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
django.setup()

import logging
import pymysql
import pymssql
from manager.statquery_manager import StatQueryManager
from domain.analysis import Analysis
from util import freq_map_builder
from util import edit_distance_util
from stat_technique.conditionalprobability_st import ConditionalProbability_ST
from stat_technique.editdistance_st import EditDistance_ST
from stat_technique.unigramprobability_st import UnigramProbability_ST
from stat_technique.normaldistribution_st import NormalDistribution_ST
from score.score_engine import ScoreEngine
from multiprocessing import Process
import multiprocessing
import time
import pprint
from manager import database_connection_manager
from data.models import CommonIssue, CommonScore, CommonStattechnique
from django.utils import timezone
from trainer.trainer import Trainer
from django.db import connection

logging.Formatter.converter = time.gmtime
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
log = logging.getLogger(__name__)

def run():
    query_manager = StatQueryManager()
    stat_queries = query_manager.get_queries()

    '''
    TODO: Aggregate logs per process to stop logs from being returned in random order
    pool = multiprocessing.Pool(6)
    r = pool.map_async(process_query_wrapper, stat_queries)
    pool.close()
    pool.join()

    '''
    for stat_query in stat_queries:
        process_query_wrapper(stat_query)


def process_query_wrapper(stat_query):
    try:
        log.info("Starting stat_query %s", stat_query.queryname)
        start = time.time()
        process_query(stat_query)
        log.info("Finished stat_query %s in %s seconds", stat_query.queryname, time.time() - start)
    except Exception as err:
        log.error("Query failed to process queryname = \"%s\"", stat_query.queryname)
        log.exception(err)

def process_query(stat_query):
    start = time.time()
    target_connection = database_connection_manager.get_connection(stat_query.database_server, stat_query.server_type)
    [freqmaps, highest_revision, trailing_revision] = freq_map_builder.build_freq_maps(stat_query, target_connection)
    freqmap = freqmaps["freqmap"]
    latest_freqmap = freqmaps["latest_freqmap"]

    stat_techniques = list()

    cp = ConditionalProbability_ST(freqmap, latest_freqmap)
    ed = EditDistance_ST(freqmap, latest_freqmap)
    up = UnigramProbability_ST(freqmap, latest_freqmap)
    stat_techniques.append(cp)
    stat_techniques.append(ed)
    stat_techniques.append(up)

    stat_query_manager = StatQueryManager()
    static_weights = stat_query_manager.get_static_weights(stat_query)
    static_weight_dict = dict()
    for weight in static_weights:
        static_weight_dict[weight.stattechnique.stattechnique] = weight.weight

    if static_weight_dict.get("Normal Distribution") is not None:
        if static_weight_dict.get("Normal Distribution") != 0.0:
            nd = NormalDistribution_ST(freqmap, latest_freqmap)
            stat_techniques.append(nd)

    stat_techniques = run_all_stat_techniques(stat_techniques)

    score_engine = ScoreEngine(None, static_weight_dict, stat_query.use_neural_network)
    issues = analyze_and_save_issues(stat_techniques, score_engine, stat_query, target_connection)
    if stat_query.auto_update_revision:
        update_most_recent_revision(stat_query, highest_revision)

    if stat_query.auto_update_trailing_revision:
       update_trailing_revision(stat_query, trailing_revision)

    #Only record time if at least one issue detected
    if len(issues) > 0:
        update_run_times(stat_query, time.time() - start)

def update_run_times(stat_query, timing):
    stat_query_manager = StatQueryManager()
    stat_query_manager.update_run_times(stat_query, timing)

def update_most_recent_revision(stat_query, highest_revision):
    stat_query_manager = StatQueryManager()
    stat_query_manager.update_most_recent_revision(stat_query, highest_revision)

def update_trailing_revision(stat_query, trailing_revision):
    stat_query_manager = StatQueryManager()
    stat_query_manager.update_trailing_revision(stat_query, trailing_revision)

def run_all_stat_techniques(stat_techniques):
    for stat_technique in stat_techniques:
        run_stat_technique(stat_technique)
    return stat_techniques

def run_stat_technique(stat_technique):
    log.debug("Starting stat_tech %s", stat_technique.get_name())
    start = time.time()
    stat_technique.process()
    log.debug("Finished stat_tech %s in %s seconds", stat_technique.get_name(), time.time() - start)

def analyze_and_save_issues(stat_techniques, score_engine, stat_query, target_connection):
    stat_technique = stat_techniques[0]
    issues = list()

    for key, bucket in stat_technique.get_latest_freqmap().items():
        for bucket_value, freq in bucket.items():
            [total_score, explanation] = build_master_scores(score_engine, stat_techniques, (key+", "+bucket_value))

            if (total_score*100) > stat_query.scorethreshold:
                string = stat_query.queryname + "\t"+key + ", " + bucket_value + "\n"

                log.debug("Overall Score:\t%s", total_score)
                for stat_techique in stat_techniques:
                    log.debug("\t%s:\t%s", stat_techique.get_name(), stat_techique.get_scores()[key+", "+bucket_value])

                context = get_context(stat_query, target_connection, key, bucket_value)

                connection.connect()
                issue, created = CommonIssue.objects.get_or_create(
                    queryid = stat_query,
                    queryvalue = (key+", "+bucket_value),
                    querykey = stat_query.queryname,

                    defaults={
                        "status": "Open",
                        "suggestion": get_suggestion(stat_techique.get_freqmap()[key], bucket_value),
                        "overall_score": (total_score*100),
                        "explanation": explanation,
                        "date_opened": timezone.now,
                        "context": context
                    }
                )

                if created:
                    issue.save()
                    for stat_techique in stat_techniques:
                        score = CommonScore.objects.create(
                            score = stat_techique.get_scores()[key+", "+bucket_value],
                            issue = issue,
                            stattechnique = CommonStattechnique.objects.get(stattechnique=stat_techique.get_name())
                        )
                        score.save()
                issues.append(issue)
    return issues

def get_context(stat_query, target_connection, key, bucket_value):
    try:
        cur = target_connection.cursor()
        key_split = key.split(',')
        params = []
        for param in key_split:
            params.append(param)
        params.append(bucket_value)
        cur.execute(stat_query.context_query, tuple(params))
        response = ""
        results = cur.fetchone()
        if results == None:
            return "error retrieving context"
        for result in results:
            response += result + ", "
        response = response[0:len(response)-2]
        log.debug("StatQuery %s context for key = \"%s\" and bucket_value = \"%s\": %s", stat_query.queryname, key, bucket_value, response)
        return response
    except:
        return "error retrieving context"

def build_master_scores(score_engine, stat_techniques, key):
    [total_score, explanation] = score_engine.get_overall_score(stat_techniques, key)
    return [total_score, explanation]

def get_suggestion(freqmap, test_bucket):
    [min_distance, suggestion] = edit_distance_util.edit_distance_comparison(freqmap, test_bucket)
    return suggestion

def train():
    trainer = Trainer()
    trainer.train_thresholds()

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Flags')
    parser.add_argument('--train', action='store_true', help='Flag to enable training mode of thresholds')

    args = parser.parse_args()

    if args.train:
        train()
    else:
        run()




