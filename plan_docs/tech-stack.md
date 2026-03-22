# workflow-orchestration-queue Technology Stack

*Generated: March 22, 2026*

This document defines the complete technology stack for the workflow-orchestration-queue system, an autonomous AI development floor that transforms GitHub Issues into verified Pull Requests without human intervention.

---

## Languages & Runtimes

### Python 3.12+
- **Role:** Primary language for all system logic
- **Use Cases:** Sentinel orchestrator, Notifier webhook receiver, data models, queue interfaces
- **Features Used:** Native async/await, improved error messages, performance enhancements
- **Package Management:** `uv` (Rust-based, fast dependency resolver)

### PowerShell Core (pwsh) / Bash
- **Role:** Shell bridge scripts and cross-platform CLI interactions
- **Use Cases:** GitHub authentication, devcontainer orchestration, remote index updates
- **Key Scripts:**
  - `scripts/devcontainer-opencode.sh` - Core worker lifecycle management
  - `scripts/gh-auth.ps1` - GitHub App token synchronization
  - `scripts/common-auth.ps1` - Shared authentication utilities
  - `scripts/update-remote-indices.ps1` - Vector index maintenance

---

## Web Frameworks

### FastAPI
- **Role:** High-performance async web framework for the webhook receiver ("The Ear")
- **Features:**
  - Native Pydantic integration for request/response validation
  - Automatic OpenAPI/Swagger documentation at `/docs`
  - Async request handling for non-blocking webhook ingestion
  - Dependency injection for queue implementations

### Uvicorn
- **Role:** ASGI server for production FastAPI deployment
- **Usage:** `uv run uvicorn notifier_service:app --reload` (development)

---

## Data Validation & Serialization

### Pydantic
- **Role:** Strict schema validation and settings management
- **Use Cases:**
  - `WorkItem` model - Unified work item across components
  - `TaskType` enum - PLAN, IMPLEMENT, BUGFIX
  - `WorkItemStatus` enum - Maps to GitHub labels
  - Settings validation at startup

---

## HTTP Client

### httpx
- **Role:** Fully asynchronous HTTP client for GitHub API calls
- **Features:**
  - Connection pooling via single `AsyncClient` instance
  - Async/await support without blocking event loop
  - Proper timeout handling
- **Implementation:** `GitHubQueue` class creates client once in `__init__()`, reuses across all calls

---

## Package Management

### uv
- **Role:** Rust-based Python package installer and dependency resolver
- **Benefits:**
  - Orders of magnitude faster than pip or poetry
  - Deterministic lockfile via `uv.lock`
  - Accelerated DevContainer build times
- **Configuration:** `pyproject.toml` defines dependencies

---

## Containerization

### Docker
- **Role:** Worker isolation and environment reproducibility
- **Features:**
  - Network isolation (dedicated bridge network)
  - Resource constraints (2 CPUs, 4GB RAM per worker)
  - Ephemeral credentials via environment variables
- **Key Configuration:** `.devcontainer/devcontainer.json`, `.github/.devcontainer/Dockerfile`

### Docker Compose
- **Role:** Multi-container orchestration for complex workloads
- **Use Case:** Running web app + database for integration testing

### DevContainers
- **Role:** High-fidelity development environment identical to human developers
- **Benefits:**
  - Eliminates "it works on my machine" discrepancies
  - Bit-for-bit identical environment for AI and humans
  - Pre-built images cached in GHCR for fast startup

---

## Agent Runtime

### opencode CLI
- **Role:** AI agent execution framework
- **Version:** 1.2.24+
- **Configuration:** `.opencode/opencode.json` defines MCP servers and agent settings
- **Usage:** `opencode --model zai-coding-plan/glm-5 --agent Orchestrator`

### MCP Servers
- **@modelcontextprotocol/server-sequential-thinking:** Step-by-step reasoning
- **@modelcontextprotocol/server-memory:** Knowledge graph persistence

---

## LLM Models

### Primary: ZhipuAI GLM-5
- **Access:** Via `ZHIPU_API_KEY` environment variable
- **Role:** Primary model for agent execution

### Secondary: Kimi (Moonshot)
- **Access:** Via `KIMI_CODE_ORCHESTRATOR_AGENT_API_KEY`
- **Role:** Alternative model for orchestration tasks

---

## CI/CD & Infrastructure

### GitHub Actions
- **Role:** Workflow automation, CI validation, deployment
- **Key Workflows:**
  - `orchestrator-agent.yml` - Agent execution pipeline
  - `validate.yml` - Lint, scan, test
  - `publish-docker.yml` - Base image publishing
  - `prebuild-devcontainer.yml` - Devcontainer image caching

### GitHub CLI (gh)
- **Role:** Programmatic GitHub API access
- **Authentication:** Via `GITHUB_TOKEN` or interactive login

### GitHub Packages (GHCR)
- **Role:** Container registry for pre-built devcontainer images
- **Images:** `ghcr.io/{org}/{repo}/devcontainer`

---

## State Management

### GitHub Issues
- **Role:** Distributed state machine ("Markdown as a Database")
- **State Labels:**
  - `agent:queued` - Awaiting pickup
  - `agent:in-progress` - Claimed by Sentinel
  - `agent:reconciling` - Stale task recovery
  - `agent:success` - Completed successfully
  - `agent:error` - Execution error
  - `agent:infra-failure` - Infrastructure failure
  - `agent:stalled-budget` - Budget exceeded

### GitHub Projects
- **Role:** Kanban board for workflow visualization
- **Project URL:** https://github.com/orgs/intel-agency/projects/14

---

## Security

### HMAC Signature Verification
- **Role:** Webhook payload validation
- **Algorithm:** SHA256 with `WEBHOOK_SECRET`
- **Header:** `X-Hub-Signature-256`

### Credential Scrubbing
- **Role:** Sanitize logs before posting to GitHub
- **Patterns:** GitHub PATs (`ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`), Bearer tokens, API keys (`sk-*`), ZhipuAI keys
- **Implementation:** `scrub_secrets()` in `src/models/work_item.py`

### GitHub App Installation Tokens
- **Role:** Scoped API access with 5,000 requests/hour limit
- **Management:** Via `scripts/gh-auth.ps1`

---

## Development Tools

### Linting & Scanning
- **gitleaks:** Secret detection
- **Markdown lint:** Documentation validation
- **Shellcheck:** Shell script validation

### Testing
- **Framework:** Shell-based tests in `test/`
- **Key Tests:**
  - `test-devcontainer-build.sh` - Container build validation
  - `test-devcontainer-tools.sh` - Tool availability checks
  - `test-prompt-assembly.sh` - Prompt template validation

---

## File Structure

```
workflow-orchestration-queue/
├── pyproject.toml           # uv dependencies
├── uv.lock                  # Deterministic lockfile
├── src/
│   ├── orchestrator_sentinel.py  # Polling & dispatch
│   ├── notifier_service.py       # Webhook receiver
│   ├── models/
│   │   └── work_item.py     # Unified data model
│   └── queue/
│       └── github_queue.py  # GitHub API queue
├── scripts/
│   ├── devcontainer-opencode.sh  # Shell bridge
│   ├── gh-auth.ps1          # GitHub auth
│   └── validate.ps1         # CI validation
├── .opencode/
│   ├── opencode.json        # Agent config
│   └── agents/              # Agent definitions
├── .devcontainer/
│   └── devcontainer.json    # Consumer devcontainer
└── .github/
    ├── workflows/           # GitHub Actions
    └── .devcontainer/       # Build-time devcontainer
```

---

## Environment Variables

### Required (MVP)
| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub App installation token |
| `GITHUB_ORG` | Target organization name |
| `GITHUB_REPO` | Target repository name |

### Optional
| Variable | Description | Default |
|----------|-------------|---------|
| `SENTINEL_BOT_LOGIN` | Bot account for locking | `""` (disabled) |
| `WEBHOOK_SECRET` | HMAC secret for Notifier | Required for Phase 2 |
| `ZHIPU_API_KEY` | ZhipuAI model access | Required for agent execution |
| `VERSION_PREFIX` | Docker image version prefix | `1.0` |

---

## References

- [Architecture Guide](./OS-APOW%20Architecture%20Guide%20v3.2.md)
- [Development Plan](./OS-APOW%20Development%20Plan%20v4.2.md)
- [Implementation Specification](./OS-APOW%20Implementation%20Specification%20v1.2.md)
- [Simplification Report](./OS-APOW%20Simplification%20Report%20v1.md)
- [Plan Review](./OS-APOW%20Plan%20Review.md)
