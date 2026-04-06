"""Tests for the WorkItem model."""

import pytest

from workflow_orchestration_queue.models.work_item import (
    TaskType,
    WorkItem,
    WorkItemStatus,
    scrub_secrets,
)


class TestTaskType:
    """Tests for TaskType enum."""

    def test_task_type_values(self) -> None:
        """Test that TaskType has expected values."""
        assert TaskType.PLAN.value == "PLAN"
        assert TaskType.IMPLEMENT.value == "IMPLEMENT"
        assert TaskType.BUGFIX.value == "BUGFIX"


class TestWorkItemStatus:
    """Tests for WorkItemStatus enum."""

    def test_status_values(self) -> None:
        """Test that WorkItemStatus has expected values."""
        assert WorkItemStatus.QUEUED.value == "agent:queued"
        assert WorkItemStatus.IN_PROGRESS.value == "agent:in-progress"
        assert WorkItemStatus.SUCCESS.value == "agent:success"
        assert WorkItemStatus.ERROR.value == "agent:error"


class TestWorkItem:
    """Tests for WorkItem model."""

    def test_create_work_item(self) -> None:
        """Test creating a WorkItem instance."""
        item = WorkItem(
            id="test-123",
            issue_number=42,
            source_url="https://github.com/test/repo/issues/42",
            context_body="Test issue body",
            target_repo_slug="test/repo",
            task_type=TaskType.IMPLEMENT,
            status=WorkItemStatus.QUEUED,
            node_id="NODE123",
        )
        assert item.id == "test-123"
        assert item.issue_number == 42
        assert item.task_type == TaskType.IMPLEMENT
        assert item.status == WorkItemStatus.QUEUED

    def test_work_item_serialization(self) -> None:
        """Test WorkItem serialization to dict."""
        item = WorkItem(
            id="test-456",
            issue_number=100,
            source_url="https://github.com/org/repo/issues/100",
            context_body="Context",
            target_repo_slug="org/repo",
            task_type=TaskType.PLAN,
            status=WorkItemStatus.IN_PROGRESS,
            node_id="NODE456",
        )
        data = item.model_dump()
        assert data["id"] == "test-456"
        assert data["task_type"] == TaskType.PLAN


class TestScrubSecrets:
    """Tests for the scrub_secrets function."""

    def test_scrub_github_pat(self) -> None:
        """Test that GitHub PATs are scrubbed."""
        # Use a FAKE key pattern that won't trigger gitleaks
        text = "Token: ghp_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE"
        result = scrub_secrets(text)
        assert "ghp_" not in result
        assert "***REDACTED***" in result

    def test_scrub_bearer_token(self) -> None:
        """Test that Bearer tokens are scrubbed."""
        text = "Authorization: Bearer abc123def456ghi789=="
        result = scrub_secrets(text)
        assert "Bearer" not in result or "***REDACTED***" in result

    def test_scrub_preserves_safe_text(self) -> None:
        """Test that safe text is preserved."""
        text = "This is a normal message without secrets"
        result = scrub_secrets(text)
        assert result == text

    def test_scrub_multiple_secrets(self) -> None:
        """Test scrubbing multiple secrets in one text."""
        # Use FAKE prefixes that won't trigger gitleaks
        text = "Key1: ghp_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE Key2: sk-FAKEFAKEFAKEFAKEFAKE"
        result = scrub_secrets(text)
        assert "ghp_" not in result
        assert "sk-FAKE" not in result
        assert result.count("***REDACTED***") >= 2

    def test_custom_replacement(self) -> None:
        """Test using a custom replacement string."""
        text = "ghp_FAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKEFAKE"
        result = scrub_secrets(text, replacement="[HIDDEN]")
        assert "[HIDDEN]" in result
