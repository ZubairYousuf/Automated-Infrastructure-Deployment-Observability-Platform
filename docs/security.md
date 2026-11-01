# Security considerations

- The API container runs as a non-root user, uses a read-only root filesystem, drops Linux capabilities, and sets resource limits.
- Secrets belong in .env or a dedicated secret store. Do not commit passwords, tokens, private keys, or production inventory.
- NGINX blocks public access to /metrics. Prometheus, Grafana, and Alertmanager bind to loopback on the Docker host.
- This demo serves HTTP on port 8080. Add TLS termination and authentication before exposing it publicly.
- Review image tags, dependencies, and CI action versions periodically; use immutable digests for hardened environments.
- The task API uses an in-memory demo store with no authentication. It is not suitable for storing sensitive information or public production workloads.
- Docker socket access and host mounts are security-sensitive. Apply least privilege on remote hosts.
- CI scanning provides additional checks but does not establish a security guarantee.
