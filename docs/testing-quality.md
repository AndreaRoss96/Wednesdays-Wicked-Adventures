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

# Specific test type
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/smoke/

# Specific test file
python -m pytest tests/unit/test_models.py
```

### Test Configuration

**pytest.ini** (`flask_app/src/pytest.ini`):
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers --cov=main --cov-report=html --cov-report=term-missing --cov-report=xml
markers =
    unit: Unit tests
    integration: Integration tests
    smoke: Smoke tests
    slow: Slow running tests
```

### Test Structure

```
flask_app/src/tests/
├── conftest.py                # Shared fixtures and test data
├── unit/
│   ├── test_auth.py           # Password hashing, role checks
│   ├── test_models.py         # User, Role, Park, Booking, Message models
│   └── test_seed_data.py      # Database seeding verification
├── integration/
│   ├── test_flow.py           # End-to-end user flows
│   ├── test_login_routes.py   # Login, register, forgot password, logout
│   └── test_main_routes.py    # Index, park detail, profile, booking, contact
└── smoke/
    └── test_smoke.py          # App startup, public routes, error handling
```

### Test Types

| Type | Purpose | Location | CI Phase |
|------|---------|----------|----------|
| **Smoke** | Verify app starts and basic routes work | `tests/smoke/` | Phase 6 (standalone) |
| **Unit** | Test individual model methods and functions | `tests/unit/` | Phase 7 (with coverage) |
| **Integration** | Test route logic, form submissions, DB operations | `tests/integration/` | Phase 7 (with coverage) |

### Test Fixtures (conftest.py)

| Fixture | Scope | Purpose |
|---------|-------|---------|
| `app` | function | Creates Flask app with TestingConfig, seeds test data, cleanup |
| `client` | function | Flask test client for HTTP requests |
| `runner` | function | CLI runner for command testing |
| `db_session` | function | Database session with transaction rollback |
| `authenticated_client` | function | Client logged in as `test@example.com` |

**Test data seeded by fixtures:**

| Entity | Details |
|--------|---------|
| Roles | user, admin |
| Test User | test@example.com / password123 |
| Admin User | admin@example.com / admin123 |
| Parks | 3 test parks (Leprechaun, Paddy, Haunted House) |

### What Each Test File Covers

**Unit Tests:**

| File | Tests |
|------|-------|
| `test_auth.py` | Password hashing with PBKDF2, role assignment, `has_role()` method |
| `test_models.py` | CRUD for User, Role, Park, Booking, Message; relationships; `to_json()` |
| `test_seed_data.py` | Seed data creates correct roles, parks, admin users |

**Integration Tests:**

| File | Tests |
|------|-------|
| `test_login_routes.py` | Login form, login POST, registration, forgot password, logout |
| `test_main_routes.py` | Homepage, park detail, profile, new booking, contact form, 404 |
| `test_flow.py` | Full user journeys: register → login → book → view bookings |

**Smoke Tests:**

| File | Tests |
|------|-------|
| `test_smoke.py` | App initialization, public routes respond, auth redirects work, contact form, error handling, template rendering, DB integrity |

### CI Pipeline Integration

**Phase 6 — Smoke Tests** (run first, fast feedback):
```bash
python -m pytest tests/smoke/ -v --tb=short --color=yes
```

**Phase 7 — Full Test Suite** (with coverage):
```bash
python -m pytest --cov=app --cov-report=xml --cov-report=term-missing
```

Coverage XML is sent to SonarCloud in Phase 8.

## Code Quality

### Flake8

Flake8 is used for Python code linting (Phase 4 of CI Pipeline).

**Running locally:**
```bash
cd flask_app/src/main
flake8 . --max-line-length=127 --exclude=venv,__pycache__
```

**CI Configuration:**

| Check Type | Rules | Blocking |
|------------|-------|----------|
| Critical errors | E9, F63, F7, F82 | **Yes** |
| Style warnings | max-complexity=10, max-line-length=127 | No |

**Critical checks explained:**

| Code | Meaning |
|------|---------|
| E9 | Runtime errors (syntax, IO) |
| F63 | Invalid test assertions |
| F7 | Syntax errors in code |
| F82 | Undefined names |

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
sonar.sources=main/app
sonar.tests=tests
sonar.python.version=3.11
sonar.python.coverage.reportPaths=coverage.xml
```

**Exclusions:** `venv`, `__pycache__`, `migrations`, `static`, `templates`

*Note: Quality gate wait is currently disabled in pipeline (`sonar.qualitygate.wait=false`).*

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
   - Phase 6: Smoke tests output
   - Phase 7: Full test results with coverage percentage

3. **Coverage Report**
   - Shows percentage of code tested
   - Identifies untested areas

4. **PR Review History**
   - Shows code review comments
   - Shows requested changes and fixes
