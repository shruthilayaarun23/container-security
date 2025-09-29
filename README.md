
# Container Security & Runtime Protection Pipeline

A DevSecOps project showcasing container vulnerability scanning, Kubernetes runtime monitoring, and threat detection with industry-standard tools.

## Overview

Pipeline demonstrates security from **build → deploy → runtime** using an intentionally vulnerable Flask app, Trivy for image scanning, and Falco for runtime detection in Kubernetes (EKS).

## Architecture

1. **Vulnerable Flask App** – intentionally insecure web app
2. **Image Scanning** – Trivy identifies CVEs in dependencies and base images
3. **Runtime Protection** – Falco monitors Kubernetes workloads

## Technologies

* Docker, AWS ECR, Amazon EKS, Helm
* Trivy (image scanning)
* Falco (runtime security)
* Python Flask (intentionally vulnerable)

## Key Features

* **Vulnerability Scanning:** 88 vulns (3 CRITICAL, 13 HIGH, etc.)
* **Runtime Detection:** alerts on sensitive file access, shell execution, privilege escalation, and network scans
* **Misconfigurations:** runs as root, excessive capabilities, secrets in env vars, permissive RBAC/netpol

## Findings

* CVEs in Flask, Pillow, Jinja2
* Runtime alerts: `/etc/shadow` access, shell spawned, password/keys search

