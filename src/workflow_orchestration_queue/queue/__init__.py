"""Queue implementations for workflow-orchestration-queue."""

from workflow_orchestration_queue.queue.github_queue import (
    GitHubQueue,
    ITaskQueue,
)

__all__ = [
    "GitHubQueue",
    "ITaskQueue",
]
