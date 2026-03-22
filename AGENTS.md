---
file: AGENTS.md
description: Project instructions for coding agents
scope: repository
---

<instructions>
  <purpose>
    <summary>
      Python-based autonomous AI development floor that transforms GitHub Issues into verified Pull Requests.
      The system consists of two main components:
      - **Sentinel**: Orchestrator that polls GitHub for queued tasks, manages worker lifecycle, and dispatches AI agents
      - **Notifier**: FastAPI webhook receiver that maps GitHub events to a unified work item queue
      On GitHub events (issues, PR comments, reviews), the `orchestrator-agent` workflow assembles a structured prompt,
      spins up a devcontainer, and runs `opencode --agent Orchestrator` to delegate work to specialist sub-agents.
    </summary>
  </purpose>

  <template_usage>
    <summary>
      This repository is a **GitHub template repo** (`intel-agency/workflow-orchestration-queue-zulu78-b`).
      New project repositories are created from it using automation scripts in the
      `nam20485/workflow-launch2` repo. The scripts clone this template, seed plan docs,
      replace template placeholders, and push — producing a ready-to-go AI-orchestrated repo.
    </summary>

    <template-clone-instances>
      Once the template has been cloned into a new instance, this file must be updated to match the new repo's specifics (e.g., name, links, instructions). 
    </template-clone-instances>

    <creation_workflow>
      <step>1. Run `./scripts/create-repo-from-slug.ps1 -Slug &lt;project-slug&gt; -Yes` from the `workflow-launch2` repo.</step>
      <step>2. That delegates to `./scripts/create-repo-with-plan-docs.ps1` which:
        - Creates a new GitHub repo from this template via `gh repo create --template intel-agency/workflow-orchestration-queue-zulu78-b`
        - Generates a random suffix for the repo name (e.g., `project-slug-bravo84`)
        - Creates repo secrets (`GEMINI_API_KEY`) and variables (`VERSION_PREFIX`)
        - Clones the new repo locally
        - Copies plan docs from `./plan_docs/&lt;slug&gt;/` into the clone's `plan_docs/` directory
        - Replaces all template placeholders (`workflow-orchestration-queue-zulu78-b` → new repo name, `intel-agency` → new owner)
        - Commits and pushes the seeded repo
      </step>
      <step>3. On push, the clone's `validate` workflow runs CI (lint, scan, tests, devcontainer build) and the `publish-docker` workflow builds and pushes the base Docker image to GHCR.</step>
      <step>4. On successful `publish-docker` completion, the `prebuild-devcontainer` workflow is triggered (via `workflow_run`) to build and push the prebuilt devcontainer image. Together, `publish-docker` → `prebuild-devcontainer` form the devcontainer prebuild caching pipeline that the `orchestrator-agent` workflow relies on to quickly spin up devcontainers.</step>
    </creation_workflow>

    <template_design_constraints>
      <rule>Template placeholders (`workflow-orchestration-queue-zulu78-b`, `intel-agency`) in file contents and paths are replaced by the creation script. Keep them consistent.</rule>
      <rule>The `validate` workflow must tolerate fresh clones where no prebuilt GHCR devcontainer image exists yet (fallback build from Dockerfile + image aliasing).</rule>
      <rule>The `plan_docs/` directory contains external-generated documents seeded at clone time. Exclude it from strict linting (markdown lint, etc.).</rule>
      <rule>The consumer `.devcontainer/devcontainer.json` references a prebuilt GHCR image. On fresh clones the image won't exist until `publish-docker` and `prebuild-devcontainer` workflows complete their first run.</rule>
    </template_design_constraints>

    <automation_scripts>
      <entry><repo>nam20485/workflow-launch2</repo><path>scripts/create-repo-from-slug.ps1</path><description>Entry point — takes a slug, resolves plan docs dir, delegates to create-repo-with-plan-docs.ps1</description></entry>
      <entry><repo>nam20485/workflow-launch2</repo><path>scripts/create-repo-with-plan-docs.ps1</path><description>Full pipeline: repo create, clone, seed docs, placeholder replace, commit, push</description></entry>
    </automation_scripts>
  </template_usage>

  <tech_stack>
    <summary>Python-based backend with FastAPI for web services and async HTTP communication.</summary>
    <runtime>Python 3.12+ (managed via uv package manager)</runtime>
    <web_framework>FastAPI — async web framework for the Notifier webhook receiver</web_framework>
    <http_client>httpx — async HTTP client for GitHub API interactions</http_client>
    <validation>Pydantic — data validation and settings management</validation>
    <package_manager>uv — Astral's fast Python package manager (replaces pip/poetry)</package_manager>
    <testing>pytest + pytest-asyncio + pytest-cov — async-aware testing with coverage</testing>
    <linting>ruff — fast Python linter (replaces flake8, isort, pyupgrade)</linting>
    <type_checking>mypy — static type checking with strict mode</type_checking>
    <containerization>Docker (Dockerfile.sentinel, Dockerfile.notifier)</containerization>
    <orchestration>
      <item>opencode CLI — agent runtime (`opencode --model zai-coding-plan/glm-5 --agent Orchestrator`)</item>
      <item>ZhipuAI GLM models via `ZHIPU_API_KEY`</item>
      <item>GitHub Actions + devcontainers/ci — workflow trigger, runner, reproducible container</item>
      <item>MCP servers: `@modelcontextprotocol/server-sequential-thinking`, `@modelcontextprotocol/server-memory`</item>
    </orchestration>
  </tech_stack>

  <repository_map>
    <!-- Source Code -->
    <entry><path>src/workflow_orchestration_queue/</path><description>Main Python package</description></entry>
    <entry><path>src/workflow_orchestration_queue/__init__.py</path><description>Package init — exports WorkItem, TaskType, WorkItemStatus, scrub_secrets</description></entry>
    <entry><path>src/workflow_orchestration_queue/sentinel.py</path><description>Sentinel Orchestrator — polls GitHub, claims tasks, manages worker lifecycle, posts heartbeats</description></entry>
    <entry><path>src/workflow_orchestration_queue/notifier.py</path><description>FastAPI webhook receiver — maps GitHub events to work queue</description></entry>
    <entry><path>src/workflow_orchestration_queue/models/</path><description>Pydantic models (WorkItem, TaskType, WorkItemStatus)</description></entry>
    <entry><path>src/workflow_orchestration_queue/models/work_item.py</path><description>Canonical data model + secret scrubbing utilities</description></entry>
    <entry><path>src/workflow_orchestration_queue/queue/</path><description>Queue implementations</description></entry>
    <entry><path>src/workflow_orchestration_queue/queue/github_queue.py</path><description>GitHub-backed work queue (ITaskQueue implementation)</description></entry>
    <!-- Tests -->
    <entry><path>tests/</path><description>pytest test suite</description></entry>
    <entry><path>tests/test_work_item.py</path><description>Tests for WorkItem model and secret scrubbing</description></entry>
    <!-- Configuration -->
    <entry><path>pyproject.toml</path><description>Project config — dependencies, scripts (sentinel, notifier), tool settings (ruff, mypy, pytest)</description></entry>
    <!-- Dockerfiles -->
    <entry><path>Dockerfile.sentinel</path><description>Container image for Sentinel orchestrator service</description></entry>
    <entry><path>Dockerfile.notifier</path><description>Container image for Notifier webhook service</description></entry>
    <!-- Workflows -->
    <entry><path>.github/workflows/validate.yml</path><description>CI workflow — lint, scan, test, devcontainer build</description></entry>
    <entry><path>.github/workflows/orchestrator-agent.yml</path><description>Primary workflow — assembles prompt, logs into GHCR, runs opencode in devcontainer</description></entry>
    <entry><path>.github/workflows/prompts/orchestrator-agent-prompt.md</path><description>Prompt template with `__EVENT_DATA__` placeholder (sed-substituted at runtime)</description></entry>
    <entry><path>.github/workflows/publish-docker.yml</path><description>Builds Dockerfile, pushes to GHCR with branch-latest and branch-&lt;VERSION_PREFIX.run_number&gt; tags</description></entry>
    <entry><path>.github/workflows/prebuild-devcontainer.yml</path><description>Layers devcontainer Features on published Docker image (triggered by workflow_run)</description></entry>
    <!-- Agent definitions -->
    <entry><path>.opencode/agents/orchestrator.md</path><description>Orchestrator — coordinates specialists, never writes code directly</description></entry>
    <entry><path>.opencode/agents/</path><description>All specialist agents (developer, code-reviewer, planner, devops-engineer, github-expert, etc.)</description></entry>
    <entry><path>.opencode/commands/</path><description>Reusable command prompts (orchestrate-new-project, grind-pr-reviews, fix-failing-workflows, etc.)</description></entry>
    <entry><path>.opencode/opencode.json</path><description>opencode config — MCP server definitions</description></entry>
    <!-- Devcontainer -->
    <entry><path>.github/.devcontainer/Dockerfile</path><description>Devcontainer image — Python, uv, opencode CLI (build context for publish-docker)</description></entry>
    <entry><path>.github/.devcontainer/devcontainer.json</path><description>Build-time devcontainer config (Dockerfile + Features: node, python, gh CLI)</description></entry>
    <entry><path>.devcontainer/devcontainer.json</path><description>Consumer devcontainer — pulls prebuilt GHCR image, forwards port 4096, and auto-starts `opencode serve` on container start</description></entry>
    <entry><path>scripts/start-opencode-server.sh</path><description>Guarded `opencode serve` bootstrapper used by the devcontainer lifecycle and workflow attach path</description></entry>
    <entry><path>scripts/run-devcontainer-orchestrator.sh</path><description>One-shot script: brings up the devcontainer, ensures the opencode server is running, and executes the orchestrator agent. Used by the workflow and can be invoked directly locally.</description></entry>
    <!-- Shell tests -->
    <entry><path>test/</path><description>Shell-based tests: devcontainer build, tool availability, prompt assembly</description></entry>
    <entry><path>test/fixtures/</path><description>Sample webhook payloads for local testing</description></entry>
    <!-- Remote instructions -->
    <entry><path>local_ai_instruction_modules/</path><description>Local instruction modules (development rules, workflows, delegation, terminal commands)</description></entry>
    <!-- Plan docs (seeded at clone time) -->
    <entry><path>plan_docs/</path><description>External-generated documents seeded at clone time — exclude from linting</description></entry>

    <opencode_server>
      <summary>
        The consumer devcontainer auto-starts `opencode serve` through `scripts/start-opencode-server.sh`.
        The server listens on port `4096` by default so host or in-container clients can attach with
        `opencode run --attach http://127.0.0.1:4096 ...` (or the forwarded host port when connecting from outside the container).
      </summary>
    </opencode_server>
  </repository_map>

  <instruction_source>
    <repository>
      <name>nam20485/agent-instructions</name>
      <branch>main</branch>
    </repository>
    <guidance>
      Remote instructions are the single source of truth. Fetch from raw URLs:
      replace `github.com/` with `raw.githubusercontent.com/` and remove `blob/`.
      Core instructions: `https://raw.githubusercontent.com/nam20485/agent-instructions/main/ai_instruction_modules/ai-core-instructions.md`
    </guidance>
    <modules>
      <module type="core" required="true" link="https://github.com/nam20485/agent-instructions/blob/main/ai_instruction_modules/ai-core-instructions.md">Core Instructions</module>
      <module type="local" required="true" path="local_ai_instruction_modules">Local AI Instructions</module>
      <module type="local" required="true" path="local_ai_instruction_modules/ai-dynamic-workflows.md">Dynamic Workflow Orchestration</module>
      <module type="local" required="true" path="local_ai_instruction_modules/ai-workflow-assignments.md">Workflow Assignments</module>
      <module type="local" required="true" path="local_ai_instruction_modules/ai-development-instructions.md">Development Instructions</module>
      <module type="optional" path="local_ai_instruction_modules/ai-terminal-commands.md">Terminal Commands</module>
    </modules>
  </instruction_source>

  <environment_setup>
    <secrets>
      <item>`GITHUB_TOKEN` — GitHub API access for Sentinel and Notifier; set in repo Settings → Secrets.</item>
      <item>`GITHUB_ORG` — GitHub organization name for Sentinel polling.</item>
      <item>`GITHUB_REPO` — GitHub repository name for Sentinel polling.</item>
      <item>`SENTINEL_BOT_LOGIN` — (optional) Bot account login for assign-then-verify locking.</item>
      <item>`WEBHOOK_SECRET` — GitHub webhook secret for Notifier signature verification.</item>
      <item>`ZHIPU_API_KEY` — ZhipuAI model access; set in repo Settings → Secrets.</item>
      <item>`KIMI_CODE_ORCHESTRATOR_AGENT_API_KEY` — Kimi (Moonshot) model access; set in repo Settings → Secrets.</item>
    </secrets>
    <devcontainer_cache>
      Image at `ghcr.io/${{ github.repository }}/devcontainer`. `publish-docker.yml` builds the raw Dockerfile;
      `prebuild-devcontainer.yml` layers Features. Login via `docker/login-action` with `GITHUB_TOKEN`.
      Set repo variable `VERSION_PREFIX` (e.g., `1.0`) for versioned tags emitted by both image publishing workflows.
    </devcontainer_cache>
  </environment_setup>

  <testing>
    <summary>pytest-based test suite with async support and coverage reporting.</summary>
    <commands>
      <command>Install dependencies: `uv sync --extra dev`</command>
      <command>Run all tests: `uv run pytest`</command>
      <command>Run with coverage: `uv run pytest --cov=src/workflow_orchestration_queue --cov-report=term-missing`</command>
      <command>Run specific test file: `uv run pytest tests/test_work_item.py -v`</command>
      <command>Run with markers: `uv run pytest -m "not slow"`</command>
    </commands>
    <configuration>
      <setting>pytest.ini_options.asyncio_mode = "auto"</setting>
      <setting>pytest.ini_options.testpaths = ["tests"]</setting>
      <setting>pytest.ini_options.addopts = "-v --tb=short"</setting>
    </configuration>
    <shell_tests>
      Shell-based tests in `test/` validate devcontainer build, tool availability, and prompt assembly:
      <command>All shell tests: `bash test/test-devcontainer-build.sh && bash test/test-devcontainer-tools.sh && bash test/test-prompt-assembly.sh`</command>
      <command>Prompt changes: `bash test/test-prompt-assembly.sh`</command>
      <command>Dockerfile changes: `bash test/test-devcontainer-tools.sh`</command>
    </shell_tests>
  </testing>

  <code_style>
    <summary>Strict code quality enforced via ruff linting and mypy type checking.</summary>
    <linting>
      <tool>ruff</tool>
      <target_version>py312</target_version>
      <line_length>100</line_length>
      <enabled_rules>
        <rule>E — pycodestyle errors</rule>
        <rule>W — pycodestyle warnings</rule>
        <rule>F — Pyflakes</rule>
        <rule>I — isort</rule>
        <rule>B — flake8-bugbear</rule>
        <rule>C4 — flake8-comprehensions</rule>
        <rule>UP — pyupgrade</rule>
        <rule>ARG — flake8-unused-arguments</rule>
        <rule>SIM — flake8-simplify</rule>
      </enabled_rules>
      <commands>
        <command>Lint check: `uv run ruff check src/ tests/`</command>
        <command>Auto-fix: `uv run ruff check --fix src/ tests/`</command>
        <command>Format check: `uv run ruff format --check src/ tests/`</command>
        <command>Format: `uv run ruff format src/ tests/`</command>
      </commands>
    </linting>
    <type_checking>
      <tool>mypy</tool>
      <mode>strict</mode>
      <python_version>3.12</python_version>
      <commands>
        <command>Type check: `uv run mypy src/`</command>
      </commands>
      <notes>
        <note>Tests have relaxed typing (`disallow_untyped_defs = false`)</note>
        <note>Missing imports ignored for third-party libraries</note>
      </notes>
    </type_checking>
  </code_style>

  <project_scripts>
    <summary>Entry points defined in pyproject.toml [project.scripts].</summary>
    <script name="sentinel">`uv run sentinel` — Run the Sentinel orchestrator (polls GitHub, dispatches workers)</script>
    <script name="notifier">`uv run notifier` — Run the Notifier webhook server (FastAPI on port 8000)</script>
    <alternative>Both can also be run as modules: `uv run python -m workflow_orchestration_queue.sentinel`</alternative>
  </project_scripts>

  <development_workflow>
    <setup>
      <step>1. Clone the repository</step>
      <step>2. Install dependencies: `uv sync --extra dev`</step>
      <step>3. Set required environment variables (see environment_setup)</step>
      <step>4. Run tests to verify setup: `uv run pytest`</step>
    </setup>
    <commands>
      <command name="Setup">`uv sync --extra dev`</command>
      <command name="Run tests">`uv run pytest`</command>
      <command name="Lint">`uv run ruff check src/ tests/`</command>
      <command name="Format">`uv run ruff format src/ tests/`</command>
      <command name="Type check">`uv run mypy src/`</command>
      <command name="Run sentinel">`uv run sentinel`</command>
      <command name="Run notifier">`uv run notifier`</command>
      <command name="Full validation">`pwsh -NoProfile -File ./scripts/validate.ps1 -All`</command>
    </commands>
  </development_workflow>

  <coding_conventions>
    <rule>Keep changes minimal and targeted.</rule>
    <rule>Do not hardcode secrets/tokens. When writing tests for credential-scrubbing or secret-detection utilities, use obviously synthetic values that will not trigger `gitleaks` (e.g., `FAKE-KEY-FOR-TESTING-00000000`). Never use prefixes that match real provider formats (`sk-`, `ghp_`, `ghs_`, `AKIA`, etc.) in test fixtures.</rule>
    <rule>Use Pydantic models for all data structures (WorkItem, TaskType, WorkItemStatus).</rule>
    <rule>Use async/await for all I/O operations (GitHub API, HTTP requests).</rule>
    <rule>Import order managed by ruff (isort) — first-party imports use `workflow_orchestration_queue`.</rule>
    <rule>Preserve the `__EVENT_DATA__` placeholder in `orchestrator-agent-prompt.md`.</rule>
    <rule>Keep orchestrator delegation-depth ≤2 and "never write code directly" constraint.</rule>
    <rule>Pin ALL GitHub Actions by full SHA to the latest release — no tag or branch references (`@v4`, `@main`). Format: `uses: owner/action@<full-40-char-SHA> # vX.Y.Z`. The trailing comment with the semver tag is mandatory for human readability. This applies to every `uses:` line in every workflow file, including third-party actions, first-party (`actions/*`), and reusable workflows. Supply-chain attacks via tag mutation are a critical threat — SHA pinning is the only mitigation. When creating or modifying workflows, look up the SHA for the latest release of each action (e.g., via `gh api repos/actions/checkout/releases/latest --jq .tag_name` then resolve to SHA) and pin to it.</rule>
    <rule>Never add duplicate top-level `name:`, `on:`, or `jobs:` keys in workflow YAML.</rule>
    <rule>`.opencode/` is checked out by `actions/checkout`; do not COPY it in the Dockerfile.</rule>
    <rule>Dockerfile lives at `.github/.devcontainer/Dockerfile`. Consumer devcontainer uses `"image:"` — no local build.</rule>
    <rule>Repository labels are defined in `.github/.labels.json`. Use `scripts/import-labels.ps1` to sync them to a repo instance. When adding new labels, add them to this file — it is the single source of truth for the label set.</rule>
    <rule>Use the `scrub_secrets()` function before posting any user-generated content to GitHub comments (R-7).</rule>
  </coding_conventions>

  <agent_specific_guardrails>
    <rule>The Orchestrator agent delegates to specialists via the `task` tool — never writes code directly.</rule>
    <rule>Prompt assembly pipeline:
      1. Read template from `.github/workflows/prompts/orchestrator-agent-prompt.md`.
      2. Prepend structured event context (event name, action, actor, repo, ref, SHA).
      3. Append raw event JSON from `${{ toJson(github.event) }}`.
      4. Write to `.assembled-orchestrator-prompt.md` and export path via `GITHUB_ENV`.
    </rule>
  </agent_specific_guardrails>

  <agent_readiness>
    <verification_protocol>
      For any non-trivial change (logic, behavior, refactors, dependency updates, config changes, multi-file edits):
      run verification, fix all failures, re-run until clean. Do not skip or suppress errors.
    </verification_protocol>

    <verification_commands>
      <!--
        MANDATORY: After every non-trivial change, run validation BEFORE commit/push.
        Do NOT commit or push until it passes. Do NOT skip steps.

        Local (runs all checks sequentially — lint, scan, test):
          pwsh -NoProfile -File ./scripts/validate.ps1 -All

        This is the SAME script that CI calls with individual switches:
          ./scripts/validate.ps1 -Lint   (CI: lint job)
          ./scripts/validate.ps1 -Scan   (CI: scan job)
          ./scripts/validate.ps1 -Test   (CI: test job)

        If a check is skipped due to a missing local tool, run:
          pwsh -NoProfile -File ./scripts/install-dev-tools.ps1

        Python-specific commands:
          uv sync --extra dev        # Install dependencies
          uv run pytest              # Run tests
          uv run ruff check src/     # Lint
          uv run mypy src/           # Type check

        | Check                  | Command                                              | When to run              |
        |========================|======================================================|==========================|
        | All (local default)    | ./scripts/validate.ps1 -All                           | Every task               |
        | Python tests           | uv run pytest                                         | After code changes       |
        | Python lint            | uv run ruff check src/ tests/                         | Quick check              |
        | Python type check      | uv run mypy src/                                      | After code changes       |
        | Scan only              | ./scripts/validate.ps1 -Scan                           | Secrets concern          |
        | Devcontainer tests     | bash test/test-devcontainer-tools.sh                   | Dockerfile changes       |
      -->
      <rule>When adding a CI workflow check, add its equivalent to scripts/validate.ps1.</rule>
    </verification_commands>

    <post_commit_monitoring>
      After push, monitor CI until green: `gh run list --limit 5`, `gh run watch <id>`, `gh run view <id> --log-failed`.
      If any workflow fails, stop feature work, triage, fix, re-verify, push. Do not mark work complete while CI is failing.
    </post_commit_monitoring>

    <pipeline_speed_policy>
      <lane name="fast_readiness" blocking="true">Build, lint/format, unit tests — keep fast for merge readiness.</lane>
      <lane name="extended_validation" blocking="false">Integration suites, security scans, dependency audits.</lane>
      <rule>Protect the fast lane from slow steps.</rule>
    </pipeline_speed_policy>
  </agent_readiness>

  <validation_before_handoff>
    <step>Run applicable tests: `uv run pytest`</step>
    <step>Run linting: `uv run ruff check src/ tests/`</step>
    <step>Run type checking: `uv run mypy src/`</step>
    <step>Run full validation: `pwsh -NoProfile -File ./scripts/validate.ps1 -All`</step>
    <step>Validate workflow YAML: `grep -c "^name:" .github/workflows/orchestrator-agent.yml  # expect 1`</step>
    <step>Summarize: what changed, what was validated, remaining risks (secret-dependent paths, image cache misses).</step>
  </validation_before_handoff>

  <pr_commit_guidelines>
    <summary>Follow conventional commit format and ensure all CI checks pass before requesting review.</summary>
    <commit_format>
      <type>feat: — new feature</type>
      <type>fix: — bug fix</type>
      <type>docs: — documentation only</type>
      <type>style: — formatting, no code change</type>
      <type>refactor: — code change without fix/feature</type>
      <type>test: — adding/updating tests</type>
      <type>chore: — maintenance, CI, dependencies</type>
    </commit_format>
    <pr_requirements>
      <requirement>All CI checks must pass (lint, scan, test)</requirement>
      <requirement>Code coverage should not decrease</requirement>
      <requirement>Type checking must pass (`uv run mypy src/`)</requirement>
      <requirement>No secrets or credentials in code</requirement>
    </pr_requirements>
  </pr_commit_guidelines>

  <tool_use_instructions>
    <instruction id="querying_microsoft_documentation">
      <applyTo>**</applyTo>
      <title>Querying Microsoft Documentation</title>
      <tools><tool>microsoft_docs_search</tool><tool>microsoft_docs_fetch</tool><tool>microsoft_code_sample_search</tool></tools>
      <guidance>
        Use these MCP tools for Microsoft technologies (C#, ASP.NET Core, .NET, EF, NuGet).
        Prioritize retrieved info over training data for newer features.
      </guidance>
    </instruction>
    <instruction id="sequential_thinking_default_usage">
      <applyTo>*</applyTo>
      <title>Sequential Thinking</title>
      <tools><tool>sequential_thinking</tool></tools>
      <guidance>
        Use for all non-trivial requests. Enables step-by-step analysis with revision, branching, and dynamic adjustment.
        Use when: breaking down complex problems, planning, architectural decisions, debugging, multi-step context.
      </guidance>
    </instruction>
    <instruction id="memory_default_usage">
      <applyTo>*</applyTo>
      <title>Knowledge Graph Memory</title>
      <tools><tool>create_entities</tool><tool>create_relations</tool><tool>add_observations</tool><tool>delete_entities</tool><tool>delete_observations</tool><tool>delete_relations</tool><tool>read_graph</tool><tool>search_nodes</tool><tool>open_nodes</tool></tools>
      <guidance>
        Use for non-trivial requests. Persist user/project context (preferences, configs, decisions, challenges, solutions).
        Entities have names, types, and observations. Relations connect entities. Search/read at task start; update after significant work.
      </guidance>
    </instruction>
  </tool_use_instructions>

  <available_tools>
    <summary>
      Tools available inside the devcontainer at runtime. Installed via
      `.github/.devcontainer/Dockerfile` unless noted otherwise.
    </summary>

    <runtimes_and_package_managers>
      <tool name="python" version="3.12+">`Python` — primary runtime for the workflow-orchestration-queue package.</tool>
      <tool name="uv" version="0.10.9+">`uv` — Astral Python package manager. Also provides `uvx` for ephemeral tool runs.</tool>
      <tool name="node" version="24.14.0 LTS">`Node.js` — JavaScript runtime. Required for MCP server packages (`npx`).</tool>
      <tool name="npm">`npm` — Node package manager (bundled with Node.js).</tool>
      <tool name="bun" version="1.3.10">`Bun` — fast JavaScript/TypeScript runtime, bundler, and package manager.</tool>
    </runtimes_and_package_managers>

    <cli_tools>
      <tool name="gh">`GitHub CLI` — interact with GitHub API (issues, PRs, repos, releases, actions). Authenticated automatically via `GITHUB_TOKEN` env var in CI; use `gh auth login --with-token` otherwise.</tool>
      <tool name="opencode" version="1.2.24">`opencode CLI` — AI agent runtime. Runs agents defined in `.opencode/agents/` with MCP server support.</tool>
      <tool name="git">`Git` — version control (system package + devcontainer feature).</tool>
    </cli_tools>

    <python_tools>
      <tool name="pytest">Testing framework — run with `uv run pytest`</tool>
      <tool name="ruff">Linter and formatter — run with `uv run ruff check` and `uv run ruff format`</tool>
      <tool name="mypy">Type checker — run with `uv run mypy src/`</tool>
    </python_tools>

    <github_authentication>
      <summary>
        GitHub API access is configured at multiple layers to support both `gh` CLI and MCP GitHub server operations.
      </summary>
      <layer name="GITHUB_TOKEN">Provided automatically by GitHub Actions. Passed into the devcontainer via `--remote-env`.</layer>
      <layer name="GITHUB_PERSONAL_ACCESS_TOKEN">Bridged from `GITHUB_TOKEN` for the `@modelcontextprotocol/server-github` MCP server, which requires this specific env var name. Set in `opencode.json` via the MCP `env` block, in `devcontainer.json` `remoteEnv`, and exported in `run_opencode_prompt.sh`.</layer>
      <layer name="gh auth login">`run_opencode_prompt.sh` authenticates the `gh` CLI via `echo "$GITHUB_TOKEN" | gh auth login --with-token` before launching opencode.</layer>
    </github_authentication>

    <scripts_directory>
      <summary>PowerShell helper scripts in `scripts/` for GitHub setup and management tasks.</summary>
      <script name="scripts/common-auth.ps1">Shared `Initialize-GitHubAuth` function — checks `gh auth status`, authenticates via PAT token (`$env:GITHUB_AUTH_TOKEN`) or interactive login.</script>
      <script name="scripts/gh-auth.ps1">Extended GitHub auth helper — supports PAT token auth via `--with-token` and interactive fallback.</script>
      <script name="scripts/import-labels.ps1">Imports labels from `.github/.labels.json` into the repository.</script>
      <script name="scripts/create-milestones.ps1">Creates project milestones from plan docs.</script>
      <script name="scripts/test-github-permissions.ps1">Verifies `GITHUB_TOKEN` has required permissions (contents, issues, PRs, packages).</script>
      <script name="scripts/query.ps1">PR review thread manager — fetches unresolved review threads from a PR, summarizes them, and can batch-reply and resolve them. Supports `--AutoResolve`, `--DryRun`, `--Interactive`, `--ReplyEach`, `--Path`, `--BodyContains` filtering. Use this instead of writing ad-hoc scripts to resolve PR review comments.</script>
      <script name="scripts/update-remote-indices.ps1">Updates remote instruction module indices.</script>
      <script name="scripts/validate.ps1">Single validation script for CI and local dev — runs lint, scan, test with individual switches or `-All`.</script>
      <script name="scripts/install-dev-tools.ps1">Installs required dev tools (actionlint, hadolint, shellcheck, gitleaks, etc.).</script>
    </scripts_directory>
  </available_tools>
</instructions>
