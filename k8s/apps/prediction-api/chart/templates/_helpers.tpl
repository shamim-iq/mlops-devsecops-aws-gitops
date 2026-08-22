{{- define "prediction-api.name" -}}
{{- .Chart.Name -}}
{{- end -}}

{{- define "prediction-api.labels" -}}
app.kubernetes.io/name: {{ include "prediction-api.name" . }}
app.kubernetes.io/part-of: {{ .Values.labels.partOf }}
{{- end -}}

{{- define "prediction-api.selectorLabels" -}}
app.kubernetes.io/name: {{ include "prediction-api.name" . }}
{{- end -}}
