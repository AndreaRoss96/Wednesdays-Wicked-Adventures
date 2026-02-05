# Testing & Quality

This document covers the testing strategy and code quality tools used in the project.

## Testing Framework

### pytest

The project uses **pytest** for all testing.

**Running tests locally:**
```bash
cd flask_app/src

# Basic run
python -m pytest

# With coverage
python -m pytest --cov=app --cov-report=term-missing

# Verbose mode
python -m pytest -v

# Specific test file
python -m pytest tests/unit/test_models.py
```

### Test Configuration

**pytest.ini** (`flask_app/src/pytest.ini`):
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts = -v --tb=short
```

### Test Structure

```
flask_app/src/tests/
├── conftest.py              # Shared fixtures
├── integration/
│   ├── test_flow.py         # End-to-end flow tests
│   ├── test_login_routes.py # Login route tests
│   └── test_main_routes.py  # Main route tests
└── unit/
    ├── test_auth.py         # Authentication tests
    ├── test_models.py       # Model tests
    └── test_seed_data.py    # Seed data tests

tests/
└── test_smoke.py            # Smoke tests for CI
```

### Test Types

| Type | Purpose | Location |
|------|---------|----------|
| Smoke Tests | Verify CI pipeline works | `tests/test_smoke.py` |
| Unit Tests | Test individual functions | `flask_app/src/tests/unit/` |
| Integration Tests | Test component interactions | `flask_app/src/tests/integration/` |

### Writing Tests

Example test structure:
```python
import pytest
from app import create_app

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

### Flake8

Flake8 is used for Python code linting.

**Running locally:**
```bash
cd flask_app/src/main
flake8 . --max-line-length=127 --exclude=venv,__pycache__
```

**CI Configuration:**
- Critical errors (E9, F63, F7, F82): Blocking
- Style warnings: Non-blocking
- Max complexity: 10
- Max line length: 127

### SonarCloud

SonarCloud performs static code analysis for:

- Code smells
- Bugs
- Vulnerabilities
- Code coverage
- Duplications

**Project:** [SonarCloud Dashboard](https://sonarcloud.io/project/overview?id=AndreaRoss96_Wednesdays-Wicked-Adventures)

**Configuration** (`flask_app/src/sonar-project.properties`):
```properties
sonar.projectKey=AndreaRoss96_Wednesdays-Wicked-Adventures
sonar.organization=andreaross96
```

**Quality Gates:**

| Metric | Threshold |
|--------|-----------|
| Coverage | Configurable |
| Duplications | < 3% |
| Maintainability Rating | A |
| Reliability Rating | A |
| Security Rating | A |

*Note: Quality gate is currently disabled due to 403 error.*

### Interpreting SonarCloud Results

**Issue Severities:**

| Severity | Action Required |
|----------|-----------------|
| Blocker | Must fix before merge |
| Critical | Must fix before merge |
| Major | Should fix |
| Minor | Nice to fix |
| Info | Informational |

### Coverage Reports

**Generating coverage locally:**
```bash
cd flask_app/src
python -m pytest --cov=app --cov-report=html
```

View report: Open `htmlcov/index.html` in browser

**CI Coverage:**
Coverage reports are generated during CI and sent to SonarCloud via:
```bash
python -m pytest --cov=app --cov-report=xml
```

## Code Review Checklist

Before approving a PR, verify:

- [ ] Tests pass locally and in CI
- [ ] New code has test coverage
- [ ] No new SonarCloud blockers/criticals
- [ ] Flake8 critical errors fixed
- [ ] Code follows project conventions
- [ ] Documentation updated if needed

## Quality Evidence for Assignment

To demonstrate quality processes:

1. **SonarCloud Dashboard Screenshot**
   - Shows quality gate status
   - Shows metrics (coverage, bugs, smells)

2. **CI Test Results**
   - Green checkmark on PR
   - Test output logs showing pytest results

3. **Coverage Report**
   - Shows percentage of code tested
   - Identifies untested areas

4. **PR Review History**
   - Shows code review comments
   - Shows requested changes and fixes
