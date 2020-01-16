from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('queries', views.queries, name='queries'),
    path('health', views.health, name='health'),
    path('issues_api', views.issues_api, name='issues_api'),
    path('issues_chart_api', views.issues_chart_api, name='issues_chart_api'),
    path('general_issue_info', views.general_issue_info, name='general_issue_info'),
    path('domain_spread_api', views.domain_spread_api, name='domain_spread_api'),
    path('change_issue_state', views.change_issue_state, name='change_issue_state')
]
