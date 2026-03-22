# workflow-orchestration-queue Architecture Overview

*Generated: March 22, 2026*

This document provides a high-level architectural overview of the workflow-orchestration-queue system, an autonomous AI development floor that transforms GitHub Issues into verified Pull Requests.

---

## Executive Summary

workflow-orchestration-queue represents a paradigm shift from **Interactive AI Coding** to **Headless Agentic Orchestration**. Traditional AI developer tools require a human-in-the-loop to navigate files, provide context, and trigger executions. workflow-orchestration-queue replaces this manual overhead with a persistent, event-driven infrastructure that transforms GitHub Issues into "Execution Orders" autonomously fulfilled by specialized AI agents.

**Success Definition:** "Zero-Touch Construction" — a user opens a single Specification Issue and, within minutes, receives a functional, test-passed branch and PR.

---

## System Architecture: The Four Pillars

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GitHub (State & Communication)                    │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  ┌───────────────┐  │
│  │   Issues    │  │    Labels    │  │   PRs       │  │   Comments    │  │
│  └──────┬──────┘  └──────┬───────┘  └──────┬──────┘  └───────┬───────┘  │
└─────────┼────────────────┼─────────────────┼─────────────────┼──────────┘
          │                │                 │                 │
          ▼                ▼                 │                 ▼
┌─────────────────────────────────────────────┐     ┌──────────────────────┐
│          THE EAR (Notifier Service)          │     │    THE HANDS (Worker) │
│  ┌────────────────────────────────────────┐  │     │  ┌─────────────────┐ │
│  │  FastAPI Webhook Receiver              │  │     │  │   DevContainer  │ │
│  │  - HMAC signature verification         │  │     │  │   - opencode    │ │
│  │  - Event parsing & triaging            │  │     │  │   - LLM Agent   │ │
│  │  - Queue initialization                │  │     │  │   - Tools       │ │
│  └────────────────────────────────────────┘  │     │  └─────────────────┘ │
└───────────────────────┬─────────────────────┘     └──────────┬───────────┘
                        │                                      │
                        ▼                                      ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                    THE BRAIN (Sentinel Orchestrator)                      │
│  ┌────────────────┐  ┌─────────────────┐  ┌────────────────────────────┐  │
│  │  Polling Loop  │→ │  Task Claiming  │→ │  Shell Bridge Dispatch    │  │
│  │  (60s cycle)   │  │ (assign-verify) │  │  devcontainer-opencode.sh │  │
│  └────────────────┘  └─────────────────┘  └────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────────────────┐   │
│  │  Heartbeat Poster  │  Status Updates  │  Error Handling            │   │
│  └────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Component Overview

### 1. The Ear (Work Event Notifier)

**Technology:** Python 3.12+, FastAPI, uv, Pydantic

**Role:** The system's sensory input for external stimuli.

**Responsibilities:**
- **Secure Webhook Ingestion:** Exposes `/webhooks/github` endpoint for GitHub events
- **Cryptographic Verification:** Validates HMAC SHA256 signatures against `WEBHOOK_SECRET`
- **Intelligent Event Triage:** Parses issue bodies to detect templates (`[Application Plan]`, `[Bugfix]`)
- **Queue Initialization:** Applies `agent:queued` label via GitHub REST API

**Security:** Every incoming request is validated before parsing. Invalid signatures receive HTTP 401 immediately.

### 2. The State (Work Queue)

**Implementation:** GitHub Issues, Labels, and Milestones

**Philosophy:** "Markdown as a Database" — using GitHub as the persistence layer provides:
- World-class audit logs
- Transparent versioning
- Built-in UI for human supervision
- Real-time intervention via commenting

**State Machine:**

| Label | State | Description |
|-------|-------|-------------|
| `agent:queued` | Waiting | Task validated, awaiting Sentinel pickup |
| `agent:in-progress` | Active | Claimed by Sentinel, execution started |
| `agent:reconciling` | Recovery | Stale task detected, being recovered |
| `agent:success` | Complete | PR created, tests passed |
| `agent:error` | Failed | Execution error during prompt phase |
| `agent:infra-failure` | Failed | Infrastructure error (container, network) |
| `agent:stalled-budget` | Stalled | Budget exceeded, requires intervention |

**Concurrency Control:** GitHub Assignees act as distributed locks. The **assign-then-verify** pattern prevents race conditions:
1. Attempt to assign `SENTINEL_BOT_LOGIN` to the issue
2. Re-fetch the issue
3. Verify the assignee matches
4. Only then proceed with task execution

### 3. The Brain (Sentinel Orchestrator)

**Technology:** Python (async background service), PowerShell, Docker CLI

**Role:** Persistent supervisor managing worker lifecycle and intent-to-command mapping.

**Lifecycle:**

1. **Polling Discovery:** Every 60 seconds, query GitHub for `agent:queued` issues
   - Jittered exponential backoff on rate limits (403/429)
   - Max backoff: 960 seconds (16 minutes)

2. **Auth Synchronization:** Run `scripts/gh-auth.ps1` before execution

3. **Shell-Bridge Protocol:**
   ```bash
   ./scripts/devcontainer-opencode.sh up      # Provision infrastructure
   ./scripts/devcontainer-opencode.sh start   # Start opencode server
   ./scripts/devcontainer-opencode.sh prompt "..."  # Dispatch workflow
   ```

4. **Workflow Mapping:** Issue type → Workflow module
   - `PLAN` → `create-app-plan.md`
   - `IMPLEMENT` → `perform-task.md`
   - `BUGFIX` → `recover-from-error.md`

5. **Telemetry:** Heartbeat comments every 5 minutes during long-running tasks

6. **Environment Reset:** Stop container between tasks (prevent state bleed)

7. **Graceful Shutdown:** Handle SIGTERM/SIGINT, finish current task, clean exit

### 4. The Hands (Opencode Worker)

**Technology:** opencode CLI, LLM (GLM-5), DevContainer

**Environment:** High-fidelity DevContainer from template repo

**Capabilities:**
- **Contextual Awareness:** Access to project structure + vector-indexed codebase
- **Instructional Logic:** Executes `.md` workflow modules from `/local_ai_instruction_modules/`
- **Verification:** Runs local test suites before PR submission

---

## Data Flow: The Happy Path

```
1. STIMULUS
   User opens GitHub Issue with [Application Plan] template
   
2. NOTIFICATION (Phase 2)
   GitHub Webhook → Notifier (FastAPI)
   
3. TRIAGE
   Notifier verifies signature, confirms template, adds agent:queued label
   
4. CLAIM
   Sentinel detects label, assigns bot account, updates to agent:in-progress
   
5. SYNC
   Sentinel runs git clone/pull to sync workspace
   
6. ENVIRONMENT CHECK
   Sentinel executes: devcontainer-opencode.sh up
   
7. DISPATCH
   Sentinel sends: devcontainer-opencode.sh prompt "Execute workflow..."
   
8. EXECUTION
   Worker reads issue, generates code, runs tests, creates PR
   
9. FINALIZE
   Worker posts completion comment
   Sentinel updates label to agent:success
```

---

## Key Architectural Decisions

### ADR-07: Standardized Shell-Bridge Execution

**Decision:** The Orchestrator interacts with the worker *exclusively* via `devcontainer-opencode.sh`.

**Rationale:** Reusing shell scripts ensures environment parity between AI agents and human developers. Re-implementing Docker logic in Python would create configuration drift.

**Consequence:** Python code remains lightweight (logic/state), while Shell handles heavy lifting (infrastructure).

### ADR-08: Polling-First Resiliency Model

**Decision:** Polling is the primary discovery mechanism; Webhooks are an optimization.

**Rationale:** Webhooks are fire-and-forget. If the server is down during an event, it's lost. Polling enables "State Reconciliation" on restart — the system self-heals by checking GitHub labels.

### ADR-09: Provider-Agnostic Interface Layer

**Decision:** Queue interactions are abstracted behind `ITaskQueue` interface.

**Rationale:** While Phase 1 targets GitHub, the architecture supports swapping to Linear, Jira, or custom queues without rewriting orchestrator logic.

---

## Security Model

### Network Isolation
- Worker containers run in dedicated Docker network
- Cannot access host network or internal subnets
- Internet access allowed for package fetching only

### Credential Scoping
- GitHub App Installation Tokens passed via temporary env vars
- Credentials destroyed when container exits
- Principle of least privilege enforced

### Credential Scrubbing
All worker output passes through `scrub_secrets()` before posting to GitHub:
- GitHub PATs: `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`
- Bearer tokens
- API keys: `sk-*`, ZhipuAI keys

### Resource Constraints
- Workers capped at 2 CPUs, 4GB RAM
- Prevents rogue agents from causing DoS on host

---

## Self-Bootstrapping Lifecycle

```
Stage 0 (Seeding)
   Manual clone of template repo + plan doc seeding
   
Stage 1 (Manual Launch)
   Developer runs: devcontainer-opencode.sh up
   
Stage 2 (Project Setup)
   Developer runs: orchestrate-dynamic-workflow project-setup
   Agent configures environment, indexes codebase
   
Stage 3 (Handover)
   Developer starts sentinel.py service
   From this point: AI manages all development via GitHub Issues
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| GitHub API Rate Limiting | GitHub App tokens (5,000/hr), caching, long-polling |
| LLM Looping/Hallucination | Max steps timeout, cost guardrails, retry counter |
| Concurrency Collisions | Assign-then-verify locking pattern |
| Container Drift | Stop containers between tasks |
| Security Injection | HMAC validation, isolated containers |

---

## Implementation Phases

### Phase 0: Seeding (Bootstrapping)
- Manual template clone and plan document seeding
- Environment configuration setup

### Phase 1: The Sentinel (MVP)
- Persistent polling service
- Shell-bridge dispatch
- Status feedback via GitHub labels/comments
- Heartbeat system for long-running tasks

### Phase 2: The Ear (Webhook Automation)
- FastAPI webhook receiver
- HMAC signature validation
- Intelligent template triaging
- Local tunneling for development

### Phase 3: Deep Orchestration
- Hierarchical task decomposition (Architect Sub-Agent)
- PR review feedback loop (autonomous correction)
- Proactive workspace indexing

---

## References

- [Technology Stack](./tech-stack.md)
- [Development Plan v4.2](./OS-APOW%20Development%20Plan%20v4.2.md)
- [Architecture Guide v3.2](./OS-APOW%20Architecture%20Guide%20v3.2.md)
- [Implementation Specification v1.2](./OS-APOW%20Implementation%20Specification%20v1.2.md)
- [Simplification Report v1](./OS-APOW%20Simplification%20Report%20v1.md)
- [Plan Review](./OS-APOW%20Plan%20Review.md)
