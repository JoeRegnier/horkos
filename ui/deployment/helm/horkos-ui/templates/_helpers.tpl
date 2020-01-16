{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
*/}}
{{- define "fullname" -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Define a context path to deploy the application with, this defaults to the chart
name unless you set a contextPath under service
*/}}
{{- define "contextpath" -}}
{{- default .Chart.Name .Values.service.contextPath | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Sets the application version to use to pull a docker tag. It defaults to the chart version
with the assumption that CI is building the chart with the same version. You can override
with the image.tag value.
*/}}
{{- define "appversion" -}}
{{- default .Chart.Version .Values.image.tag -}}
{{- end -}}

