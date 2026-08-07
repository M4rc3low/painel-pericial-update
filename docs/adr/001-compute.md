# ADR 001 - ECS Fargate instead of a lift-and-shift EC2 host

## Status
Accepted for target architecture.

## Context
The legacy application combines a Streamlit UI, a Windows launcher and browser automation. A single EC2 VM would reproduce the desktop architecture but preserve OS coupling and operational overhead.

## Decision
Split web and collector workloads into containers and run them as separate ECS Fargate workloads.

## Consequences
- No server/AMI patching for application compute.
- Independent scaling and failure domains for web and collector.
- Browser automation can use a purpose-built Playwright image.
- Interactive login/session requirements need a separate design decision.
