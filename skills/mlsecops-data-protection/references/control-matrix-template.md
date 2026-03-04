# Data Control Matrix Template

| Data Source | Sensitivity | Provenance Control | Access Control | Retention Rule | Poisoning Check | Privacy Control |
|---|---|---|---|---|---|---|
| transactions-stream | high | immutable snapshots + hash | RBAC + audit | 365 days | batch anomaly gate | pseudonymization |
