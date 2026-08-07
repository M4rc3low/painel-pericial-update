# ADR 002 - RDS PostgreSQL instead of SQLite

## Status
Accepted for target architecture.

## Context
SQLite is appropriate for a single local process but becomes a bottleneck for concurrent containers and managed backup/recovery.

## Decision
Use PostgreSQL on Amazon RDS for the cloud environment while keeping SQLite as an optional local developer mode.

## Consequences
- Managed backups and point-in-time recovery options.
- Network access and credentials must be controlled through VPC security groups and Secrets Manager.
- Schema migrations should be introduced before production use.
