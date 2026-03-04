# Observability and IR Toolkit

| Tool | Use |
|---|---|
| [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | Normalize and route telemetry across services |
| [Falco](https://github.com/falcosecurity/falco) | Runtime threat detection for container and host activity |
| [AVID](https://github.com/aidfoundation/avid) | AI vulnerability taxonomy and knowledge |
| [incidentdatabase.ai](https://incidentdatabase.ai/) | Real-world AI incident examples |
| [MITRE ATLAS](https://atlas.mitre.org/) | Detection use case mapping and taxonomy alignment |
| [OWASP AI Exchange](https://owasp.org/www-project-ai/) | Community references and pattern sharing |
| [Prometheus](https://github.com/prometheus/prometheus) | Metrics time-series and alert thresholds |
| [Grafana](https://github.com/grafana/grafana) | Alert dashboards and incident visualization |
| [Loki](https://github.com/grafana/loki) | Log aggregation for model and policy logs |
| [ClickHouse](https://github.com/ClickHouse/ClickHouse) | High-volume telemetry analytics and incident hunting |
| [SigNoz](https://github.com/SigNoz/signoz) | Open distributed tracing/observability stack |
| [Kibana + ELK](https://github.com/elastic/kibana) | Search, correlation, and timeline investigations |
| [Wazuh](https://github.com/wazuh/wazuh) | Host security monitoring and alerting |
| [TheHive Project](https://github.com/TheHive-Project/TheHive) | Case management for security incidents |
| [Shuffle](https://github.com/Shuffle/Shuffle) | IR workflow automation and alert response |
| [Sigma](https://github.com/SigmaHQ/sigma) | Detection rule grammar for prompt abuse and model-query anomalies |
| [Elastic Beats](https://github.com/elastic/beats) | Endpoint-to-backend telemetry and anomaly shipping for model services |

## Execution Pattern
1. Define telemetry fields tied to model/version.
2. Create detections for prioritized abuse paths.
3. Build and exercise response playbooks.
4. Track MTTR and detection quality over time.
