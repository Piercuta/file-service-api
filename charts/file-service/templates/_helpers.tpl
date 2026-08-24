{{- define "file-service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "file-service.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- include "file-service.name" . }}
{{- end }}
{{- end }}

{{- define "file-service.labels" -}}
app.kubernetes.io/name: {{ include "file-service.name" . }}
app.kubernetes.io/component: files
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "file-service.selectorLabels" -}}
app.kubernetes.io/name: {{ include "file-service.name" . }}
{{- end }}

{{- define "file-service.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "file-service.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
