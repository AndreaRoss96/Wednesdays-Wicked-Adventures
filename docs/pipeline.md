# CI/CD Pipeline

This document describes the Continuous Integration and Continuous Deployment pipeline for the project.

## Pipeline Overview

The project uses a single comprehensive GitHub Actions workflow (`pipeline.yaml`) that runs on every feature branch push and pull request to main.

## Triggers

| Event | Branches | Action |
|-------|----------|--------|
| Push | `feature/*` | Run full pipeline |
| Pull Request | `main` | Run full pipeline |
| Manual | Any | `workflow_dispatch` |

## Pipeline Jobs

The workflow contains 3 jobs:

```
┌──────────────────────────────────┐
│   Job 1: CI/CD Pipeline          │
├──────────────────────────────────┤
│  3. Setup Environment            │
│  4. Flake8 Linting               │
│  5. Bandit (SAST)                │
│  6. Smoke Tests                  │
│  7. Full Tests + Coverage        │
│  8. SonarCloud Analysis          │
│  9. Pipeline Summary             │
└───────────────┬──────────────────┘
                │ (on success)
┌───────────────▼──────────────────┐
│   Job 2: Docker Build & Test     │
├──────────────────────────────────┤
│  1. Build Docker Image           │
│  2. Trivy Vulnerability Scan     │
│  4. Test Docker Container        │
│  5. DAST Scan (Nuclei)           │
│  7. Cleanup                      │
│  8. Docker Job Summary           │
└──────────────────────────────────┘

┌──────────────────────────────────┐
│   Job 3: Build Documentation     │  (runs in parallel)
├──────────────────────────────────┤
│  Validate docs structure         │
│  mkdocs build --strict           │
│  Upload docs-site artifact       │
└──────────────────────────────────┘
```

## Job 1: CI/CD Pipeline Phases

## Phase Details

### Phase 3: Setup Environment

- Creates Python virtual environment
- Installs dependencies from `requirements.txt`
- Ensures pytest is available
- Uses secrets: `SECRET_KEY`, `SEED_ADMIN_PASSWORD`

### Phase 4: Code Quality - Flake8

**Critical checks (blocking):**
- E9: Runtime errors
- F63: Invalid test assertions
- F7: Syntax errors
- F82: Undefined names

**Style checks (non-blocking):**
- Max complexity: 10
- Max line length: 127

### Phase 5: Security Scan (SAST)

- Tool: Bandit
- Scans Python code for security vulnerabilities
- Generates JSON report (`bandit-results.json`)
- See [Security](security.md) for details

### Phase 6: Smoke Tests

- Runs `tests/smoke/test_smoke.py` first for fast feedback
- Verifies app starts and basic routes work
- Runs before full test suite

### Phase 7: Full Tests + Coverage

- Framework: pytest
- Coverage: pytest-cov (`--cov=app --cov-report=xml`)
- Reports: XML (for SonarCloud) and terminal output
- Working directory: `flask_app/src`
- See [Testing & Quality](testing-quality.md) for details

### Phase 8: SonarCloud

- Static code analysis
- Quality gate (currently disabled due to 403 error)
- Organization: `andreaross96`
- Project: `AndreaRoss96_Wednesdays-Wicked-Adventures`

## Job 2: Docker Build & Test

This job runs **after** Job 1 succeeds (`needs: ci-pipeline`).

| Phase | Action | Details |
|-------|--------|---------|
| Build Docker Image | Build `wicked-adventures:latest` | Verifies Dockerfile, setup.py, MANIFEST.in |
| Trivy Scan | Scan image for CVEs | HIGH + CRITICAL severity, artifact: `trivy-reports` |
| Test Container | Run container, test HTTP | Port 5000, waits 15s, checks response |
| DAST (Nuclei) | Scan running app | 3 scans: critical vulns, headers, exposed panels |
| Cleanup | Stop/remove container | Always runs |

**Artifacts produced:**
- `trivy-reports` — Container vulnerability report (7 days)
- `dast-reports` — DAST scan results + summary (7 days)

See [Security](security.md) for detailed security tool documentation.

## Job 3: Build Documentation

Runs **in parallel** with other jobs.

| Step | Action |
|------|--------|
| Validate structure | Checks `mkdocs.yml`, `docs/`, `docs/index.md` exist |
| Build docs | `mkdocs build --strict` (fails on broken links) |
| Upload artifact | `docs-site` (7 days) |

## Branching Strategy

### Branch Flow

```
feature/SCRUM-XX-description
        │
        ▼
      [PR] ───► CI Pipeline runs
        │
        ▼
       main ───► Production ready
```

### Branch Naming Convention

All feature branches must follow the pattern:
```
feature/SCRUM-XX-short-description
```

Example: `feature/SCRUM-42-add-booking-validation`

### Rules

- **Never commit directly to main**
- All changes must go through Pull Requests
- Minimum 1 approval required
- CI checks must pass before merge

## Environment Variables & Secrets

| Secret | Purpose |
|--------|---------|
| `SECRET_KEY` | Flask session security |
| `SEED_ADMIN_PASSWORD` | Admin user password for seeding |
| `SONAR_TOKEN` | SonarCloud authentication |
| `GITHUB_TOKEN` | GitHub API access (auto-provided) |

## Viewing Pipeline Results

### GitHub Actions UI

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select the workflow run
4. View logs and status for each phase

### Pipeline Summary

**Job 1 summary:**
```
Setup Environment....: success
Flake8 Linting.......: success
Security Scan........: success
Test Execution.......: success
Overall Status.......: success
```

**Job 2 summary:**
```
Docker Build.........: success
Trivy Scan...........: success
Container Test.......: success
DAST Security Scan...: success
Overall Status.......: success
```

### Artifacts

| Artifact | Source | Retention |
|----------|--------|-----------|
| `security-reports` | Bandit JSON report | Default |
| `trivy-reports` | Trivy JSON + table | 7 days |
| `dast-reports` | Nuclei scans + summary | 7 days |
| `docs-site` | Built documentation HTML | 7 days |

## Pull Request Process

### PR Requirements

Every PR must include:

```markdown
## Summary
Brief description of changes

## Jira ticket
SCRUM-XX

## How to test
1. Step-by-step testing instructions

## Risk / impact
Description of potential risks

## Rollback plan
How to revert if needed
```

### Required Checks

Before merging:
- [ ] CI pipeline passed
- [ ] Code review approval (minimum 1)
- [ ] Jira ticket updated

## Definition of Done

A task is considered done when:

1. PR approved by code reviewer
2. All CI checks passed
3. Jira ticket updated
4. Documentation updated (if applicable)
