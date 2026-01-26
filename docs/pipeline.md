# CI/CD Pipeline

This document describes the Continuous Integration and Continuous Deployment pipeline for the project.

## Branching Strategy

### Branch Flow

```
feature/SCRUM-XX-description
        │
        ▼
      [PR] ──► Code Review + CI Checks
        │
        ▼
       UAT ──► User Acceptance Testing
        │
        ▼
       main ──► Production
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

## GitHub Actions Workflows

### CI Pipeline (`ci.yaml`)

**Triggers:**
- Pull requests to `main` branch

**Jobs:**

| Step | Action |
|------|--------|
| Checkout | Clone repository |
| Setup Python | Install Python 3.11 |
| Install dependencies | pip install from requirements.txt |
| Run tests | pytest -q |

```yaml
name: CI
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r flask_app/src/requirements.txt
      - name: Run tests
        run: pytest -q
```

### Documentation Pipeline (`docs.yaml`)

**Triggers:**
- Pull requests to `main` or `uat`
- Push to `main` or `uat`

**Jobs:**

| Step | Action |
|------|--------|
| Checkout | Clone repository |
| Setup Python | Install Python 3.11 |
| Install MkDocs | pip install mkdocs mkdocs-material |
| Build docs | mkdocs build |
| Upload artifact | Upload docs-site as artifact |

## Viewing Pipeline Results

### GitHub Actions UI

1. Go to repository on GitHub
2. Click **Actions** tab
3. Select the workflow run
4. View logs and status

### Artifacts

Documentation builds are uploaded as artifacts:
- Artifact name: `docs-site`
- Contains: Built HTML documentation
- Retention: 7 days

To download:
1. Go to Actions → completed workflow run
2. Scroll to **Artifacts** section
3. Click `docs-site` to download

## Pull Request Process

### PR Template

Every PR must include:

```markdown
## Summary
Brief description of changes

## Jira ticket
SCRUM-XX

## How to test
1. Step-by-step testing instructions
2. ...

## Risk / impact
Description of potential risks

## Rollback plan
How to revert if needed
```

### Required Checks

Before merging, these must pass:
- [ ] CI tests (pytest)
- [ ] Documentation build
- [ ] Code review approval

## Definition of Done

A task is considered done when:

1. PR approved by code reviewer
2. All CI checks passed
3. Jira ticket updated
4. Documentation updated (if applicable)

## Pipeline Logs & Evidence

For assignment evidence, capture:

1. **Screenshot of green CI run** - Shows tests passed
2. **Screenshot of docs artifact** - Shows documentation built
3. **PR merge history** - Shows governance process
4. **Branch protection rules** - Shows required checks

Access logs:
- GitHub → Actions → Select workflow → Select job → View logs
