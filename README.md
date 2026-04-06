# workflow-orchestration-queue

**Python-based autonomous AI development floor that transforms GitHub Issues into verified Pull Requests.**

[![Validate](https://github.com/intel-agency/workflow-orchestration-queue-zulu78-b/actions/workflows/validate.yml/badge.svg)](https://github.com/intel-agency/workflow-orchestration-queue-zulu78-b/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

workflow-orchestration-queue is an autonomous AI development system that:

- **Listens** for GitHub webhook events (issues, comments, reviews)
- **Parses** intent from structured issue templates
- **Dispatches** AI agents to implement changes in devcontainers
- **Reports** progress via GitHub labels and comments
- **Delivers** verified Pull Requests

### Key Components

| Component | Technology | Role |
|-----------|------------|------|
| **Sentinel** | Python 3.12+ | Polling orchestrator, task claiming, worker lifecycle |
| **Notifier** | FastAPI | Webhook receiver, event triage, queue initialization |
| **Queue** | GitHub Issues | State machine using labels as status indicators |
| **Worker** | opencode CLI | AI agent execution in devcontainers |

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker (for containerized execution)
- GitHub App with repo permissions

### Installation

```bash
# Clone the repository
git clone https://github.com/intel-agency/workflow-orchestration-queue-zulu78-b.git
cd workflow-orchestration-queue-zulu78-b

# Install dependencies with uv
uv sync

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

### Running Locally

```bash
# Start the notifier service
uv run python -m workflow_orchestration_queue.notifier

# Or start the sentinel orchestrator
uv run python -m workflow_orchestration_queue.sentinel
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Architecture

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
└───────────────────────────────────────────────────────────────────────────┘
```

## State Machine

GitHub labels drive the work item lifecycle:

| Label | State | Description |
|-------|-------|-------------|
| `agent:queued` | Waiting | Task validated, awaiting Sentinel pickup |
| `agent:in-progress` | Active | Claimed by Sentinel, execution started |
| `agent:reconciling` | Recovery | Stale task detected, being recovered |
| `agent:success` | Complete | PR created, tests passed |
| `agent:error` | Failed | Execution error during prompt phase |
| `agent:infra-failure` | Failed | Infrastructure error (container, network) |
| `agent:stalled-budget` | Stalled | Budget exceeded, requires intervention |

## API Reference

### Notifier Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhooks/github` | POST | GitHub webhook handler |
| `/health` | GET | Health check |
| `/` | GET | API info |
| `/docs` | GET | OpenAPI documentation |

### Sentinel CLI

```bash
# Run sentinel with environment variables
GITHUB_TOKEN=xxx GITHUB_ORG=myorg GITHUB_REPO=myrepo \
  uv run python -m workflow_orchestration_queue.sentinel
```

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/workflow_orchestration_queue

# Run specific test file
uv run pytest tests/test_work_item.py -v
```

### Code Quality

```bash
# Lint with ruff
uv run ruff check src/

# Format code
uv run ruff format src/

# Type check with mypy
uv run mypy src/
```

### Validation

```powershell
# Run all validation (lint + scan + test)
pwsh -NoProfile -File ./scripts/validate.ps1 -All
```

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | GitHub App installation token |
| `GITHUB_ORG` | Yes | Target organization name |
| `GITHUB_REPO` | Yes | Target repository name |
| `WEBHOOK_SECRET` | Yes | HMAC secret for webhook validation |
| `SENTINEL_BOT_LOGIN` | No | Bot account for distributed locking |
| `ZHIPU_API_KEY` | No | ZhipuAI LLM access key |

## Documentation

- [Architecture Overview](plan_docs/architecture.md)
- [Technology Stack](plan_docs/tech-stack.md)
- [Validation Guide](docs/README.validation.md)
- [AI Repository Summary](.ai-repository-summary.md)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run validation (`pwsh -NoProfile -File ./scripts/validate.ps1 -All`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Package management with [uv](https://docs.astral.sh/uv/)
- AI agent runtime via [opencode CLI](https://github.com/opencode-ai/opencode)
