# Workflow Execution Plan: project-setup

**Repository:** intel-agency/workflow-orchestration-queue-zulu78-b  
**Dynamic Workflow:** project-setup  
**Generated:** March 22, 2026  
**Status:** Ready for Execution

---

## 1. Overview

### Workflow Purpose

The `project-setup` dynamic workflow initiates a new repository for autonomous development. It transforms a seeded template repository (from `workflow-orchestration-queue-zulu78-b`) into a fully configured project ready for AI-driven development.

### Project: workflow-orchestration-queue

**workflow-orchestration-queue** is an autonomous development floor system for AI agents. It represents a paradigm shift from "Interactive AI Coding" to "Headless Agentic Orchestration" — transforming GitHub Issues into execution orders that are autonomously fulfilled by specialized AI agents without human intervention.

The system is designed to be **Self-Bootstrapping**: once the initial Sentinel is deployed, the system uses its own orchestration capabilities to build and refine its remaining components.

---

## 2. Project Context Summary

### System Architecture (The Four Pillars)

| Component | Role | Technology |
|-----------|------|------------|
| **The Ear** (Notifier) | Webhook receiver for event-driven intake | FastAPI, Pydantic, HMAC validation |
| **The State** (Work Queue) | Distributed state via GitHub Issues & Labels | GitHub REST API, "Markdown as Database" |
| **The Brain** (Sentinel) | Persistent polling, task claiming, dispatch | Python asyncio, Shell Bridge |
| **The Hands** (Worker) | Code execution in isolated environment | opencode CLI, DevContainer, LLM |

### Development Phases

| Phase | Name | Description |
|-------|------|-------------|
| **Phase 0** | Seeding | Manual clone and plan seeding (already complete) |
| **Phase 1** | The Sentinel (MVP) | Autonomous polling & shell-bridge execution |
| **Phase 2** | The Ear | FastAPI webhook automation for instant intake |
| **Phase 3** | Deep Orchestration | Hierarchical decomposition & self-healing |

### Key Technical Decisions

1. **Script-First Integration (ADR 07):** Sentinel uses `devcontainer-opencode.sh` exclusively for worker orchestration
2. **Polling-First Resiliency (ADR 08):** Webhooks are optimization; polling ensures self-healing on restart
3. **Provider-Agnostic Interface (ADR 09):** `ITaskQueue` abstraction enables future provider swapping (Linear, Jira)
4. **Assign-Then-Verify Locking:** Distributed task claiming prevents race conditions

### Existing Reference Implementation

The `plan_docs/` directory contains reference implementations:
- `orchestrator_sentinel.py` — Phase 1 Sentinel implementation
- `notifier_service.py` — Phase 2 Notifier implementation
- `src/models/work_item.py` — Unified data model
- `src/queue/github_queue.py` — Consolidated GitHub queue

### Simplification Report Applied

Key simplifications from `OS-APOW Simplification Report v1.md`:
- Reduced env vars from 10 to 3 required (`GITHUB_TOKEN`, `GITHUB_ORG`, `SENTINEL_BOT_LOGIN`)
- Hardcoded environment reset to `"stop"` mode
- Removed cross-repo polling (future phase)
- Consolidated queue classes to `src/queue/github_queue.py`
- Removed IPv4 scrubbing from credential scrubber
- Dropped "encrypted" log prose
- Moved Phase 3 features to Future Work appendix

---

## 3. Assignment Execution Plan

### Execution Sequence

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         project-setup Workflow                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [pre-script-begin]                                                          │
│       │                                                                      │
│       ▼                                                                      │
│  ┌─────────────────────────┐                                                │
│  │ create-workflow-plan    │ ◄── CURRENT ASSIGNMENT                         │
│  │ (THIS DOCUMENT)         │                                                │
│  └───────────┬─────────────┘                                                │
│              │                                                               │
│  [main-script]                                                               │
│              │                                                               │
│              ▼                                                               │
│  ┌─────────────────────────┐                                                │
│  │ 1. init-existing-       │ ← Branch creation, GitHub Project,            │
│  │    repository           │   Labels, PR scaffold                          │
│  └───────────┬─────────────┘                                                │
│              │                                                               │
│              ▼                                                               │
│  ┌─────────────────────────┐                                                │
│  │ 2. create-app-plan      │ ← Analyze plan_docs, create implementation    │
│  │                         │   issue with milestones                        │
│  └───────────┬─────────────┘                                                │
│              │                                                               │
│              ▼                                                               │
│  ┌─────────────────────────┐                                                │
│  │ 3. create-project-      │ ← Scaffold src/, tests/, Docker, CI/CD        │
│  │    structure            │   Create .ai-repository-summary.md             │
│  └───────────┬─────────────┘                                                │
│              │                                                               │
│              ▼                                                               │
│  ┌─────────────────────────┐                                                │
│  │ 4. create-agents-md-    │ ← Create AGENTS.md for AI agent context       │
│  │    file                 │                                                │
│  └───────────┬─────────────┘                                                │
│              │                                                               │
│              ▼                                                               │
│  ┌─────────────────────────┐                                                │
│  │ 5. debrief-and-document │ ← Capture learnings, execution trace,         │
│  │                         │   commit final report                          │
│  └─────────────────────────┘                                                │
│                                                                              │
│  [post-assignment-complete] (after each assignment)                          │
│       │                                                                      │
│       ├── validate-assignment-completion                                     │
│       └── report-progress                                                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Assignment Details

---

#### Assignment 0: create-workflow-plan (CURRENT)

| Attribute | Value |
|-----------|-------|
| **ID** | `create-workflow-plan` |
| **Trigger** | `pre-script-begin` event |
| **Goal** | Create comprehensive workflow execution plan documenting all assignments |
| **Status** | IN PROGRESS |

**Key Criteria:**
- [ ] Read project-setup dynamic workflow definition
- [ ] Trace all 5 assignments and fetch their definitions
- [ ] Read all plan_docs/ for project context
- [ ] Produce workflow-plan.md with overview, context, assignment plan, sequencing
- [ ] Commit with message: `docs: add workflow execution plan for project-setup`

**Dependencies:** None (first assignment)

**Risks:**
| Risk | Mitigation |
|------|------------|
| Incomplete plan docs | Fetch all .md files in plan_docs/; note any gaps |
| Assignment definition fetch failure | Use webfetch with fallback; document unavailable assignments |

---

#### Assignment 1: init-existing-repository

| Attribute | Value |
|-----------|-------|
| **ID** | `init-existing-repository` |
| **Trigger** | Main script, first assignment |
| **Goal** | Initialize repository with GitHub Project, labels, and PR scaffold |
| **Estimated Duration** | 15-30 minutes |

**Key Criteria:**
1. Create new branch named `dynamic-workflow-project-setup`
2. Create GitHub Project (Board template) with columns: Not Started, In Progress, In Review, Done
3. Link project to repository
4. Import labels from `.github/.labels.json` via `scripts/import-labels.ps1`
5. Rename workspace file: `ai-new-app-template.code-workspace` → `<repo-name>.code-workspace`
6. Update devcontainer name in `.devcontainer/devcontainer.json`
7. Create PR from branch to `main`

**Dependencies:**
- GitHub authentication with scopes: `repo`, `project`, `read:project`, `read:user`, `user:email`
- `gh` CLI installed and authenticated
- `.github/.labels.json` file exists

**Risks:**
| Risk | Mitigation |
|------|------------|
| Branch creation fails | Stop immediately; report error; do not proceed |
| Label import fails | Verify `.github/.labels.json` exists; check `gh auth status` |
| PR creation fails ("No commits") | Ensure at least one commit pushed before PR creation |
| GitHub Project creation fails | Verify `project` scope; run `scripts/test-github-permissions.ps1` |

**Verification Commands:**
```powershell
# Verify permissions before starting
./scripts/test-github-permissions.ps1 -Owner intel-agency

# Verify label import
gh label list --repo intel-agency/workflow-orchestration-queue-zulu78-b
```

---

#### Assignment 2: create-app-plan

| Attribute | Value |
|-----------|-------|
| **ID** | `create-app-plan` |
| **Trigger** | After `init-existing-repository` completes |
| **Goal** | Create comprehensive implementation plan from plan_docs/ as GitHub Issue |
| **Estimated Duration** | 30-60 minutes |

**Key Criteria:**
1. Analyze `plan_docs/` (Development Plan v4.2, Architecture Guide v3.2, Implementation Spec v1.2)
2. Document tech stack in `plan_docs/tech-stack.md`
3. Document architecture in `plan_docs/architecture.md`
4. Create implementation issue using `.github/ISSUE_TEMPLATE/application-plan.md`
5. Create milestones for each phase (Phase 1, Phase 2, Phase 3)
6. Link issue to GitHub Project
7. Apply labels: `planning`, `documentation`, `implementation:ready`

**Important Constraints:**
- **PLANNING ONLY** — no implementation code
- Do NOT create .csproj, .sln, or source code files
- Do NOT create application directory structures

**Dependencies:**
- `init-existing-repository` completed (labels available, project created)
- `plan_docs/` directory populated with OS-APOW documents

**Risks:**
| Risk | Mitigation |
|------|------------|
| Plan template missing | Use template from remote URL or create from Appendix A |
| Milestone creation fails | Use `gh api` or `gh milestone create` |
| Issue not linked to project | Verify project number; use `gh project item-add` |

**Reference Examples:**
- https://github.com/nam20485/advanced-memory3/issues/12
- https://github.com/nam20485/support-assistant/issues/2

---

#### Assignment 3: create-project-structure

| Attribute | Value |
|-----------|-------|
| **ID** | `create-project-structure` |
| **Trigger** | After `create-app-plan` approved |
| **Goal** | Create actual project scaffolding (solution structure, Docker, CI/CD, docs) |
| **Estimated Duration** | 45-90 minutes |

**Key Criteria:**
1. Create Python project structure:
   ```
   /
   ├── pyproject.toml
   ├── uv.lock
   ├── src/
   │   ├── orchestrator_sentinel.py
   │   ├── notifier_service.py
   │   ├── models/
   │   │   └── work_item.py
   │   └── queue/
   │       └── github_queue.py
   ├── tests/
   ├── scripts/
   └── local_ai_instruction_modules/
   ```
2. Create `Dockerfile` and `docker-compose.yml` (use Python stdlib for healthchecks)
3. Create `.github/workflows/` with CI/CD (actions pinned to SHA)
4. Create `README.md` and `docs/` structure
5. Create `.ai-repository-summary.md` at repository root
6. Verify build succeeds, Docker configs valid
7. All GitHub Actions workflows have SHA-pinned actions

**Dependencies:**
- `create-app-plan` completed and approved
- Tech stack documented (Python 3.12+, FastAPI, uv, httpx, Pydantic)

**Risks:**
| Risk | Mitigation |
|------|------------|
| Docker healthcheck with curl | Use Python stdlib: `python -c "import urllib.request..."` |
| uv editable install fails | Ensure `COPY src/ ./src/` before `uv pip install -e .` |
| Actions not SHA-pinned | Use `gh api` to resolve SHA for each action |
| Build verification fails | Run `uv sync` and `uv run pytest` locally |

**Critical Constraints:**
- All `uses:` in workflows MUST use full 40-char SHA with version comment
- Format: `uses: owner/action@<sha> # vX.Y.Z`

---

#### Assignment 4: create-agents-md-file

| Attribute | Value |
|-----------|-------|
| **ID** | `create-agents-md-file` |
| **Trigger** | After `create-project-structure` completed |
| **Goal** | Create AGENTS.md for AI coding agent context |
| **Estimated Duration** | 15-30 minutes |

**Key Criteria:**
1. Create `AGENTS.md` at repository root
2. Include sections:
   - Project Overview
   - Setup Commands (install, build, run, test, lint)
   - Project Structure (directory tree)
   - Code Style
   - Testing Instructions
   - Architecture Notes
   - PR and Commit Guidelines
   - Common Pitfalls
3. All listed commands are validated by running them
4. File uses standard Markdown with agent-focused language

**Dependencies:**
- `create-project-structure` completed (commands can be validated)
- README.md and `.ai-repository-summary.md` exist for cross-reference

**Risks:**
| Risk | Mitigation |
|------|------------|
| Commands don't work | Test each command; update if needed |
| Duplicate content with README | Complement, don't copy; link where appropriate |
| Missing tech stack details | Reference `plan_docs/tech-stack.md` |

---

#### Assignment 5: debrief-and-document

| Attribute | Value |
|-----------|-------|
| **ID** | `debrief-and-document` |
| **Trigger** | After all main assignments complete |
| **Goal** | Capture learnings, deviations, and recommendations |
| **Estimated Duration** | 20-40 minutes |

**Key Criteria:**
1. Create debrief report using structured template (12 sections)
2. Document all deviations from assignments
3. Create execution trace: `debrief-and-document/trace.md`
4. Include ACTION ITEMS for plan-impacting findings
5. Review with stakeholder and obtain approval
6. Commit and push report

**Required Report Sections:**
1. Executive Summary
2. Workflow Overview (table of all assignments)
3. Key Deliverables
4. Lessons Learned
5. What Worked Well
6. What Could Be Improved
7. Errors Encountered and Resolutions
8. Complex Steps and Challenges
9. Suggested Changes
10. Metrics and Statistics
11. Future Recommendations
12. Conclusion

**Dependencies:**
- All previous assignments completed

**Risks:**
| Risk | Mitigation |
|------|------------|
| Incomplete trace | Capture terminal output throughout workflow |
| Missing deviations | Review each assignment's acceptance criteria |

---

## 4. Sequencing Diagram

```
Time ──────────────────────────────────────────────────────────────────────►

     ┌──────────────────────────────────────────────────────────────────┐
     │                    pre-script-begin                               │
     │  ┌─────────────────────┐                                         │
     │  │ create-workflow-plan │                                        │
     │  └──────────┬──────────┘                                         │
     └─────────────┼────────────────────────────────────────────────────┘
                   │
                   ▼
     ┌──────────────────────────────────────────────────────────────────┐
     │                       main-script                                │
     │                                                                  │
     │  ┌─────────────────────┐                                        │
     │  │ init-existing-      │ ──► validate-assignment-completion     │
     │  │ repository          │ ──► report-progress                    │
     │  └──────────┬──────────┘                                        │
     │             │                                                    │
     │             ▼                                                    │
     │  ┌─────────────────────┐                                        │
     │  │ create-app-plan     │ ──► validate-assignment-completion     │
     │  │ (planning only)     │ ──► report-progress                    │
     │  └──────────┬──────────┘                                        │
     │             │                                                    │
     │             ▼                                                    │
     │  ┌─────────────────────┐                                        │
     │  │ create-project-     │ ──► validate-assignment-completion     │
     │  │ structure           │ ──► report-progress                    │
     │  └──────────┬──────────┘                                        │
     │             │                                                    │
     │             ▼                                                    │
     │  ┌─────────────────────┐                                        │
     │  │ create-agents-md-   │ ──► validate-assignment-completion     │
     │  │ file                │ ──► report-progress                    │
     │  └──────────┬──────────┘                                        │
     │             │                                                    │
     │             ▼                                                    │
     │  ┌─────────────────────┐                                        │
     │  │ debrief-and-document│ ──► validate-assignment-completion     │
     │  │                     │ ──► report-progress                    │
     │  └──────────┬──────────┘                                        │
     │             │                                                    │
     └─────────────┼────────────────────────────────────────────────────┘
                   │
                   ▼
              MERGE PR
```

---

## 5. Dependency Graph

```
create-workflow-plan (pre-script)
         │
         ▼
init-existing-repository
         │
         ├─► [GitHub Project created]
         ├─► [Labels imported]
         ├─► [Branch created]
         └─► [PR scaffold created]
         │
         ▼
create-app-plan ────────────┐
         │                  │
         ├─► [tech-stack.md]│
         ├─► [architecture.md]
         ├─► [Implementation Issue]
         └─► [Milestones created]
         │
         ▼
create-project-structure ◄──┘ (uses tech-stack.md)
         │
         ├─► [src/ structure]
         ├─► [Docker configs]
         ├─► [CI/CD workflows]
         ├─► [README.md]
         └─► [.ai-repository-summary.md]
         │
         ▼
create-agents-md-file ◄────── (validates commands)
         │
         └─► [AGENTS.md]
         │
         ▼
debrief-and-document
         │
         ├─► [debrief-and-document/trace.md]
         └─► [Debrief Report]
         │
         ▼
     MERGE PR
```

---

## 6. Critical Directives

### Action SHA Pinning (MANDATORY)

All GitHub Actions workflows created or modified during this workflow MUST pin actions to the specific commit SHA of their latest release.

**Correct:**
```yaml
uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1
```

**Incorrect:**
```yaml
uses: actions/checkout@v4
uses: actions/checkout@main
```

### Credential Scrubbing

All log output posted to GitHub issue comments MUST be passed through `scrub_secrets()` utility before posting. The scrubber strips patterns matching:
- `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*` (GitHub tokens)
- `Bearer`, `token` (auth headers)
- `sk-*` (OpenAI-style keys)
- ZhipuAI keys

### Environment Variables

**Required (3):**
- `GITHUB_TOKEN` — GitHub API authentication
- `GITHUB_ORG` — Organization name
- `SENTINEL_BOT_LOGIN` — Bot account for assign-then-verify locking

**Optional:**
- `WEBHOOK_SECRET` — For notifier service

---

## 7. Open Questions

| # | Question | Context | Resolution |
|---|----------|---------|------------|
| 1 | Should reference implementations in `plan_docs/` be copied to `src/` or used as templates? | `orchestrator_sentinel.py` and `notifier_service.py` exist in plan_docs/ | Copy to src/ during `create-project-structure`; reference impls become actual source |
| 2 | What is the target Python version for pyproject.toml? | Plan says 3.12+ | Use `requires-python = ">=3.12"` |
| 3 | Should Phase 2 (Notifier) and Phase 3 features be included in initial scaffolding? | Plan focuses on Phase 1 MVP | Include stub files for Phase 2/3; mark with TODO comments |
| 4 | What is the expected test framework? | Plan mentions tests but not framework | Use `pytest` with `pytest-asyncio` |

---

## 8. Acceptance Criteria Summary

The workflow is complete when:

- [ ] `create-workflow-plan` — This document committed
- [ ] `init-existing-repository` — Branch, Project, Labels, PR created
- [ ] `create-app-plan` — Implementation issue with milestones created
- [ ] `create-project-structure` — Full project scaffolding committed
- [ ] `create-agents-md-file` — AGENTS.md created and validated
- [ ] `debrief-and-document` — Debrief report committed
- [ ] All post-assignment-complete events executed
- [ ] PR merged to `main`

---

## 9. References

- [Dynamic Workflow: project-setup](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md)
- [Assignment: init-existing-repository](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/init-existing-repository.md)
- [Assignment: create-app-plan](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/create-app-plan.md)
- [Assignment: create-project-structure](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/create-project-structure.md)
- [Assignment: create-agents-md-file](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/create-agents-md-file.md)
- [Assignment: debrief-and-document](https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-workflow-assignments/debrief-and-document.md)
- [AGENTS.md Specification](https://agents.md/)

---

*Generated by Planner Agent | workflow-orchestration-queue-zulu78-b*
