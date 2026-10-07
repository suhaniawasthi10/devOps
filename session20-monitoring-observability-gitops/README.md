# Session 20 — Monitoring, observability and GitOps

**Suhani Awasthi · 24BCS10260**

The complete runnable implementation is shared with the final project:
- [Instrumented Notes app](../final-devops-project/application): request counters/latency, process CPU/memory, structured logs and health checks.
- [Monitoring stack and commands](../final-devops-project/monitoring/README.md): Prometheus, alert rules and Alertmanager UI.
- [GitOps manifests and workflow](../final-devops-project/gitops/README.md): Argo CD, scoped project, image promotion, drift recovery and Git rollback.

| Pillar | What it records | Useful question | Common tools |
|---|---|---|---|
| Metrics | Numeric time series | Is request rate, CPU, memory or latency changing? | Prometheus, Grafana |
| Logs | Individual events and errors | What happened for this request? | Structured application logs, Loki, Elasticsearch |
| Traces | Linked spans across a request path | Which dependency or hop caused latency? | OpenTelemetry, Jaeger, Tempo |

Monitoring checks known health signals and thresholds; observability combines evidence to investigate unexpected behavior. In Kubernetes, application metrics explain request behavior, kubelet/cAdvisor metrics explain resource use, and kube-state-metrics describes object state. Pod restart counts, Events and container logs complement those signals. Correlating timestamp and request ID helps follow a single operation.

This app implements metrics and logs. Its request ID is a correlation aid, not a distributed trace implementation. Traces are documented here as required; no tracing backend is claimed. Prometheus graphs and Alertmanager show local alerts without sending messages to anyone.

GitOps uses declarative configuration, versioned review and continuous reconciliation. Git is the desired-state record; Argo CD compares it with live state and applies changes. CI builds/tests/scans an image; promotion updates its immutable tag in Git; Argo deploys it. Rollback reverts the Git change. This differs from a one-time kubectl apply, which does not continually correct drift.

During the later session capture healthy scrape targets, request/CPU/memory graphs, logs, a firing/resolved alert, Argo Healthy/Synced state, deliberate drift and restoration. No runtime or screenshot evidence is fabricated.
