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

## Pipeline Phases

```
┌─────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline                        │
├─────────────────────────────────────────────────────────┤
│  1. Checkout Code                                        │
│       ↓                                                  │
│  2. Setup Python 3.11                                    │
│       ↓                                                  │
│  3. Setup Environment (venv + dependencies)              │
│       ↓                                                  │
│  4. Code Quality - Flake8 Linting                       │
│       ↓                                                  │
│  5. Security Scan (SAST) - Bandit                       │
│       ↓                                                  │
│  6. Run Tests - pytest with coverage                    │
│       ↓                                                  │
│  7. SonarCloud Analysis                                  │
│       ↓                                                  │
│  8. Pipeline Summary                                     │
└─────────────────────────────────────────────────────────┘
```

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

### Phase 6: Testing

- Framework: pytest
- Coverage: pytest-cov
- Reports: XML and terminal output
- Working directory: `flask_app/src`

### Phase 7: SonarCloud

- Static code analysis
- Quality gate (currently disabled due to 403 error)
- Organization: `andreaross96`
- Project: `AndreaRoss96_Wednesdays-Wicked-Adventures`

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

The final phase outputs a summary:
```
Results:
--------
Setup Environment....: success
Flake8 Linting.......: success
Security Scan........: success
Test Execution.......: success

Overall Status.......: success
```

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
