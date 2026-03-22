# API Reference

## Notifier Service

The Notifier is a FastAPI-based webhook receiver that handles GitHub events.

### Base URL

```
http://localhost:8000
```

### Endpoints

#### POST /webhooks/github

Handle GitHub webhook events.

**Headers:**
- `X-GitHub-Event`: Event type (e.g., `issues`, `push`, `pull_request`)
- `X-Hub-Signature-256`: HMAC SHA256 signature (required)

**Request Body:** GitHub webhook payload (JSON)

**Response:**

```json
// Accepted
{
  "status": "accepted",
  "item_id": "12345678"
}

// Ignored
{
  "status": "ignored",
  "reason": "No actionable OS-APOW event mapping found"
}

// Unauthorized
{
  "detail": "Invalid signature"
}
```

**Supported Events:**

| Event | Action | Trigger Condition |
|-------|--------|-------------------|
| `issues` | `opened` | Issue with `[Application Plan]` in title or `agent:plan` label |

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "online",
  "system": "workflow-orchestration-queue Notifier"
}
```

#### GET /

API information.

**Response:**
```json
{
  "name": "workflow-orchestration-queue Notifier",
  "version": "0.1.0",
  "docs": "/docs"
}
```

#### GET /docs

OpenAPI/Swagger documentation (interactive).

## Sentinel Service

The Sentinel is a background polling service with no HTTP API. It:

1. Polls GitHub for issues labeled `agent:queued`
2. Claims tasks using assign-then-verify locking
3. Dispatches workers via shell bridge
4. Updates status via GitHub labels

### Configuration

| Environment Variable | Required | Description |
|---------------------|----------|-------------|
| `GITHUB_TOKEN` | Yes | GitHub App installation token |
| `GITHUB_ORG` | Yes | Target organization |
| `GITHUB_REPO` | Yes | Target repository |
| `SENTINEL_BOT_LOGIN` | No | Bot account for locking |
| `POLL_INTERVAL` | No | Polling interval in seconds (default: 60) |

### Workflow Mapping

| TaskType | Workflow File |
|----------|---------------|
| `PLAN` | `create-app-plan.md` |
| `IMPLEMENT` | `perform-task.md` |
| `BUGFIX` | `recover-from-error.md` |

## Queue Interface

### ITaskQueue

Abstract interface for queue implementations.

```python
class ITaskQueue(ABC):
    @abstractmethod
    async def add_to_queue(self, item: WorkItem) -> bool: ...

    @abstractmethod
    async def fetch_queued_tasks(self) -> list[WorkItem]: ...

    @abstractmethod
    async def update_status(
        self, item: WorkItem, status: WorkItemStatus, comment: str | None = None
    ) -> None: ...
```

### GitHubQueue

GitHub Issues-based queue implementation.

**Additional Methods:**

| Method | Description |
|--------|-------------|
| `claim_task(item, sentinel_id, bot_login)` | Distributed locking via assign-then-verify |
| `post_heartbeat(item, sentinel_id, elapsed_secs)` | Post progress comment |
| `close()` | Release connection pool |

## Data Models

### WorkItem

```python
class WorkItem(BaseModel):
    id: str                    # GitHub issue ID
    issue_number: int          # Issue number
    source_url: str            # Issue URL
    context_body: str          # Issue body
    target_repo_slug: str      # org/repo
    task_type: TaskType        # PLAN, IMPLEMENT, BUGFIX
    status: WorkItemStatus     # Current status
    node_id: str               # GraphQL node ID
```

### TaskType

```python
class TaskType(str, Enum):
    PLAN = "PLAN"
    IMPLEMENT = "IMPLEMENT"
    BUGFIX = "BUGFIX"
```

### WorkItemStatus

```python
class WorkItemStatus(str, Enum):
    QUEUED = "agent:queued"
    IN_PROGRESS = "agent:in-progress"
    RECONCILING = "agent:reconciling"
    SUCCESS = "agent:success"
    ERROR = "agent:error"
    INFRA_FAILURE = "agent:infra-failure"
    STALLED_BUDGET = "agent:stalled-budget"
```

## Utilities

### scrub_secrets()

Sanitize text for safe posting to GitHub.

```python
def scrub_secrets(text: str, replacement: str = "***REDACTED***") -> str
```

**Patterns scrubbed:**
- GitHub PATs: `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`
- Bearer tokens
- API keys: `sk-*`, ZhipuAI keys
