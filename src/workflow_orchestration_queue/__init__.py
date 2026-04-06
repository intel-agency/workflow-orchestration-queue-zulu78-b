"""
workflow-orchestration-queue

Python-based autonomous AI development floor that transforms GitHub Issues
into verified Pull Requests without human intervention.
"""

__version__ = "0.1.0"
__author__ = "Intel Agency"

from workflow_orchestration_queue.models.work_item import (
    TaskType,
    WorkItem,
    WorkItemStatus,
    scrub_secrets,
)

__all__ = [
    "__version__",
    "__author__",
    "TaskType",
    "WorkItem",
    "WorkItemStatus",
    "scrub_secrets",
]
