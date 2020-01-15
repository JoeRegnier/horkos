from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Issue, Query, Score, StaticWeight, StatTechnique
from django.db.models import Prefetch, Count, Avg
from django.db import models
from django.core import serializers
import time
import json


# Create your views here.
def index(request):
    view_dict = dict()
    return render(request, 'ui/index.html', view_dict)

def queries(request):
    view_dict = dict()
    issue_status_filter = request.GET.get('filters', '')
    issue_status_filter = issue_status_filter.split(",")
    queries = Query.objects.annotate(issue_count=models.Sum(
        models.Case(
            models.When(issue__status__in=issue_status_filter, then=1),
            default=0, output_field=models.IntegerField()
        )
    )).values()
    databases = Query.objects.values_list('database').distinct()
    view_dict['queries'] = list(queries)
    view_dict['staticweights'] = list(StaticWeight.objects.values())
    view_dict['stattechniques'] = list(StatTechnique.objects.values())
    view_dict['databases'] = list(databases)

    return JsonResponse(view_dict, status=200)

def issues_api(request):
    view_dict = dict()
    query_id = request.GET.get('query_id', -1)
    if query_id == -1:
        return JsonResponse(view_dict, status=400)
    issue_status_filter = request.GET.get('filters', '')
    issue_status_filter = issue_status_filter.split(",")

    sortby = request.GET.get('sortby', 'score')
    if sortby.lower() == 'date':
        view_dict["issues"] = list(Issue.objects.filter(queryID_id=query_id).filter(status__in=issue_status_filter).order_by('-date_opened').values())
    else:
        view_dict["issues"] = list(Issue.objects.filter(queryID_id=query_id).filter(status__in=issue_status_filter).order_by('-overall_score').values())

    view_dict["scores"] = list(Score.objects.filter(issue__queryID_id=query_id).filter(issue__status__in=issue_status_filter).values())

    return JsonResponse(view_dict, status=200)

def issues_chart_api(request):
    view_dict = dict()
    issue_status_filter = request.GET.get('filters', '')
    issue_status_filter = issue_status_filter.split(",")
    query_id = request.GET.get('query_id', -1)
    if query_id == -1:
        view_dict["issues"] = list(Issue.objects.filter(status__in=issue_status_filter).order_by('date_opened').values('id','queryID_id', 'date_opened', 'status'))
        return JsonResponse(view_dict, status=200)
    view_dict["issues"] = list(Issue.objects.filter(queryID_id=query_id).filter(status__in=issue_status_filter).order_by('date_opened').values('id','queryID_id', 'date_opened', 'status'))
    return JsonResponse(view_dict, status=200)

def general_issue_info(request):
    view_dict = dict()
    query_id = request.GET.get('query_id', -1)
    if query_id == '-1':
        view_dict["avg_open_score"] = str(Issue.objects.filter(status='Open').aggregate(Avg('overall_score'))["overall_score__avg"])
        view_dict["avg_verified_score"] = str(Issue.objects.filter(status='Verified').aggregate(Avg('overall_score'))["overall_score__avg"])
        view_dict["avg_ignored_score"] =  str(Issue.objects.filter(status='Ignored').aggregate(Avg('overall_score'))["overall_score__avg"])
        view_dict["avg_technique_scores"] = list(Score.objects.values().filter())
        return JsonResponse(view_dict, status=200)

    view_dict["avg_open_score"] = str(Issue.objects.filter(queryID_id=query_id).filter(status='Open').aggregate(Avg('overall_score'))["overall_score__avg"])
    view_dict["avg_verified_score"] = str(Issue.objects.filter(queryID_id=query_id).filter(status='Verified').aggregate(Avg('overall_score'))["overall_score__avg"])
    view_dict["avg_ignored_score"] =  str(Issue.objects.filter(queryID_id=query_id).filter(status='Ignored').aggregate(Avg('overall_score'))["overall_score__avg"])
    return JsonResponse(view_dict, status=200)

def domain_spread_api(request):
    issue_status_filter = request.GET.get('filters', '')
    issue_status_filter = issue_status_filter.split(",")
    queries = Query.objects.annotate(issue_count=models.Sum(
        models.Case(
            models.When(issue__status__in=issue_status_filter, then=1),
            default=0, output_field=models.IntegerField()
        )
    )).values()
    domain_map = dict()
    for query in queries:
        if domain_map.get(query['database']) != None:
            domain_map[query['database']] = domain_map[query['database']] + query['issue_count']
        else:
            domain_map[query['database']] = query['issue_count']

    return JsonResponse(domain_map, status=200)

def health(request):
    return JsonResponse({'health': 'up'}, status=200)

def change_issue_state(request):
    state = request.GET.get('status', 'Open')
    issue_id = request.GET.get('id', '1')
    try:
        issue = Issue.objects.get(pk = issue_id)
        issue.status = state
        issue.save()
        return JsonResponse({'issue_id':issue_id,'status':issue.status}, status=200)
    except:
        return JsonResponse({'issue_id':issue_id,'message':"failed"}, status=500)


def specific_issue(request):
    view_dict = dict()
    issue_id = request.GET.get('id', '-1')
    view_dict["issue"] = Issue.objects.get(pk=issue_id)
    view_dict["query"] = Query.objects.get(pk=view_dict["issue"].queryID_id)
    view_dict["scores"] = Score.objects.filter(issue_id=view_dict["issue"].id)

    return render(request, 'ui/specific_issue.html', view_dict)