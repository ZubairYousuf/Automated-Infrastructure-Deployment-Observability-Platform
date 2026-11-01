# Deployment guide

## Prerequisites
Docker Engine and Docker Compose v2 for local usage. For remote deployment, use Ubuntu 22.04+ with SSH access, Ansible installed on the control machine, and an image accessible to the target.

## Local
1. Copy .env.example to .env.
2. Replace GRAFANA_ADMIN_PASSWORD with a unique password.
3. Run `docker compose up --build -d`.
4. Check `curl -f http://localhost:8080/health/ready`.
5. Visit Grafana at http://127.0.0.1:3000 and Prometheus at http://127.0.0.1:9090.

## Ubuntu VM
1. Copy infra/ansible/inventory.ini.example to infra/ansible/inventory.ini and set host and SSH user.
2. Install required collections: `ansible-galaxy collection install -r infra/ansible/requirements.yml`.
3. Run `ansible-playbook -i infra/ansible/inventory.ini infra/ansible/site.yml -e 'grafana_admin_password=YOUR_UNIQUE_PASSWORD' -e 'app_image=YOUR_IMAGE'`.
4. Configure host firewall rules and SSH key access before exposing services.
5. Deploy a new immutable image using `sudo CLOUDOPS_DIR=/opt/cloudops bash scripts/deploy.sh IMAGE_REF` from a copy of the script on the target host.

## Caution
The Ansible playbook is a reference implementation. Verify that your Ubuntu package repositories provide Docker Compose v2. For local-only image builds, the VM must have the image built or loaded before `--no-build` startup. Do not expose Grafana, Prometheus, or Alertmanager to the public internet without access controls and TLS.
