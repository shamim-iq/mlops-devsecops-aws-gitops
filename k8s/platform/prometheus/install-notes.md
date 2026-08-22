# Prometheus Install Notes

Prometheus must scrape pods with these annotations:

```text
prometheus.io/scrape: "true"
prometheus.io/path: /metrics
prometheus.io/port: "8000"
```

The analysis template expects Prometheus at `http://prometheus-server.monitoring.svc.cluster.local`. Update the template if the Helm release creates a different service name.
