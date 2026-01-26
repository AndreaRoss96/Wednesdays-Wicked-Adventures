# Testing & Quality

This document covers the testing strategy and code quality tools used in the project.

## Testing Framework

### pytest

The project uses **pytest** for all testing.

**Running tests locally:**
```bash
# Basic run
pytest

# Quiet mode (less output)
pytest -q

# Verbose mode (more details)
pytest -v

# Specific test file
pytest tests/test_smoke.py

# With coverage report
pytest --cov=flask_app
```

### Test Structure

```
Wednesdays-Wicked-Adventures/
├── tests/
│   └── test_smoke.py          # Smoke tests
└── flask_app/
    └── src/
        └── unittest/
            └── app_tests.py   # Unit tests
```

### Test Types

| Type | Purpose | Location |
|------|---------|----------|
| Smoke Tests | Verify CI pipeline works | `tests/test_smoke.py` |
| Unit Tests | Test individual functions | `flask_app/src/unittest/` |
| Integration Tests | Test component interactions | Planned |

### Writing Tests

Example test structure:
```python
import pytest
from flask_app.src.main.app import create_app

def test_app_creates():
    """Test that app factory creates application."""
    app = create_app()
    assert app is not None

def test_homepage_loads(client):
    """Test homepage returns 200."""
    response = client.get('/')
    assert response.status_code == 200
```

## Code Quality

### SonarCloud

SonarCloud performs static code analysis for:

- Code smells
- Bugs
- Vulnerabilities
- Code coverage
- Duplications

**Dashboard:** [SonarCloud Project](https://sonarcloud.io) (link TBD)

**Quality Gates:**

| Metric | Threshold |
|--------|-----------|
| Coverage | > 80% |
| Duplications | < 3% |
| Maintainability Rating | A |
| Reliability Rating | A |
| Security Rating | A |

### Interpreting SonarCloud Results

**Issue Severities:**

| Severity | Action Required |
|----------|-----------------|
| Blocker | Must fix before merge |
| Critical | Must fix before merge |
| Major | Should fix |
| Minor | Nice to fix |
| Info | Informational |

**Common Findings:**

1. **Code Smells** - Maintainability issues
   - Fix: Refactor code for clarity

2. **Cognitive Complexity** - Function too complex
   - Fix: Break into smaller functions

3. **Duplicated Code** - Copy-paste detected
   - Fix: Extract common logic

### Coverage Reports

**Generating coverage locally:**
```bash
pip install pytest-cov
pytest --cov=flask_app --cov-report=html
```

View report: Open `htmlcov/index.html` in browser

**Coverage in CI:**
Coverage reports are generated during CI and uploaded to SonarCloud.

## Code Review Checklist

Before approving a PR, verify:

- [ ] Tests pass locally and in CI
- [ ] New code has test coverage
- [ ] No new SonarCloud blockers/criticals
- [ ] Code follows project conventions
- [ ] Documentation updated if needed

## Quality Evidence for Assignment

To demonstrate quality processes:

1. **SonarCloud Dashboard Screenshot**
   - Shows quality gate status
   - Shows metrics (coverage, bugs, smells)

2. **CI Test Results**
   - Green checkmark on PR
   - Test output logs

3. **Coverage Report**
   - Shows percentage of code tested
   - Identifies untested areas

4. **PR Review History**
   - Shows code review comments
   - Shows requested changes and fixes
