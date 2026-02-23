# Security

This document describes the security measures and tools used in the project.

## Security Pipeline Overview

The project implements a multi-layered security approach across two pipeline jobs:

```
Job 1: CI Pipeline
  └── Phase 5: Bandit (SAST) --> Scan source code for vulnerabilities

Job 2: Docker Build & Test
  ├── Phase 2: Trivy --> Scan Docker image for CVEs
  └── Phase 5: Nuclei (DAST) --> Scan running application
```

## SAST - Static Application Security Testing

### Bandit

**Bandit** scans Python source code for common security issues.

**Running locally:**
```bash
cd flask_app/src
pip install bandit
bandit -r ./main/app --skip B101 -f json -o Bandit/bandit-results.json
```

**CI Integration (Phase 5 of CI Pipeline):**

| Setting | Value |
|---------|-------|
| Target | `main/app` directory |
| Skipped checks | B101 (assert statements in tests) |
| Output | JSON report in `Bandit/bandit-results.json` |
| Artifact | `security-reports` |

**Summary output in CI:**
```
Total files scanned: ...
Total issues found: ...
High severity: ...
Medium severity: ...
Low severity: ...
```

**What Bandit Checks:**

| Check ID | Description |
|----------|-------------|
| B102 | exec_used - Use of exec |
| B103 | set_bad_file_permissions |
| B104 | hardcoded_bind_all_interfaces |
| B105 | hardcoded_password_string |
| B106 | hardcoded_password_funcarg |
| B107 | hardcoded_password_default |
| B108 | hardcoded_tmp_directory |
| B110 | try_except_pass |
| B112 | try_except_continue |

**Severity Levels:**

| Level | Action |
|-------|--------|
| HIGH | Must fix before merge |
| MEDIUM | Should fix |
| LOW | Review and decide |

## Container Scanning - Trivy

**Trivy** scans the Docker image for known vulnerabilities (CVEs) in OS packages and dependencies.

**CI Integration (Phase 2 of Docker job):**

| Setting | Value |
|---------|-------|
| Image scanned | `wicked-adventures:latest` |
| Severity filter | HIGH, CRITICAL only |
| Output formats | Table (human-readable) + JSON (parsing) |
| Artifact | `trivy-reports` (7-day retention) |

**Running locally:**
```bash
# Build the image first
cd flask_app/src
docker build -t wicked-adventures:latest .

# Scan with Trivy
trivy image --severity HIGH,CRITICAL wicked-adventures:latest
```

**Summary output in CI:**
```
CRITICAL: 0
HIGH:     2
TOTAL:    2
```

**What Trivy Detects:**

- Vulnerable OS packages in the Docker image
- Known CVEs in Python dependencies
- Outdated base image components

## DAST - Dynamic Application Security Testing

### Nuclei

**Nuclei** by ProjectDiscovery scans the running application for vulnerabilities, missing headers, and exposed panels.

**CI Integration (Phase 5 of Docker job):**

The pipeline starts the Docker container, then runs 3 Nuclei scans against `http://localhost:5000`:

| Scan | Templates | Severity | Timeout |
|------|-----------|----------|---------|
| Critical vulnerabilities | `http/security-misconfiguration/` | critical | 90s |
| Security headers | `http/missing-headers/` | medium, high | 60s |
| Exposed panels | `http/exposed-panels/` | medium, high, critical | 60s |

**Artifact:** `dast-reports` (7-day retention) containing:
- `critical-scan.json` - Critical vulnerability findings
- `headers-scan.json` - Missing security headers
- `panels-scan.json` - Exposed admin/debug panels
- `summary.txt` - Consolidated report with severity counts

**Running locally:**
```bash
# Start the application
docker run -d --name test-app -p 5000:5000 \
  -e SECRET_KEY=xxx -e SEED_ADMIN_PASSWORD=xxx \
  wicked-adventures:latest

# Run Nuclei scan
docker run --rm projectdiscovery/nuclei:latest \
  -u http://host.docker.internal:5000 \
  -t http/missing-headers/ \
  -severity medium,high

# Cleanup
docker stop test-app && docker rm test-app
```

## Application Security

### Password Security

Passwords are hashed using **PBKDF2-SHA256** (via Werkzeug):

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing password
hashed = generate_password_hash(password, method='pbkdf2:sha256')

# Verifying password
is_valid = check_password_hash(stored_hash, provided_password)
```

**Security practices:**
- Passwords are never stored in plain text
- PBKDF2 with SHA256 is used for hashing
- No reversible encryption is used

### Authentication

**Flask-Login** manages user sessions:

- Session-based authentication
- `@login_required` decorator for protected routes
- Automatic session management
- Role-based access control via `has_role()` method

**Protected routes require login:**
- Profile pages
- Booking pages
- Admin panel

### CSRF Protection

**Cross-Site Request Forgery** protection via Flask-WTF:

| Environment | CSRF Status |
|-------------|-------------|
| Development | **Enabled** |
| Testing | Disabled (for automated tests) |
| Production | **Enabled** |

### Secret Management

**Environment Variables:**

| Variable | Purpose | Required In |
|----------|---------|-------------|
| `SECRET_KEY` | Flask session encryption | All environments |
| `SEED_ADMIN_PASSWORD` | Admin user seeding | Dev/CI |
| `SONAR_TOKEN` | SonarCloud auth | CI only |

**Production Requirements:**
```python
class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or None

    @classmethod
    def init_app(cls, app):
        if not cls.SECRET_KEY:
            raise RuntimeError("CRITICAL: SECRET_KEY must be set in production!")
```

### Admin Panel Security

Flask-Admin is protected by role-based access:

```python
class AppModelView(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and
                current_user.has_role('admin'))

    def inaccessible_callback(self, name, **kwargs):
        flash('ADMIN ACCESS ONLY!')
        return redirect(url_for("login.login"))
```

## Security Checklist

Before deploying to production:

- [ ] No hardcoded secrets in code
- [ ] Passwords properly hashed (PBKDF2)
- [ ] CSRF protection enabled
- [ ] SECRET_KEY set from environment
- [ ] SEED_ADMIN_PASSWORD set from environment
- [ ] SQL injection prevention (using ORM)
- [ ] XSS prevention (Jinja2 template escaping)
- [ ] Bandit scan passed (no HIGH findings)
- [ ] Trivy scan reviewed (no unpatched CRITICAL CVEs)
- [ ] Nuclei scan reviewed (no exposed panels)
- [ ] Dependencies up to date

## Security Evidence for Assignment

To demonstrate security processes:

1. **Bandit Report (SAST)**
   - CI logs showing scan results
   - `security-reports` artifact with `bandit-results.json`
   - Severity breakdown (HIGH/MEDIUM/LOW)

2. **Trivy Report (Container Scanning)**
   - CI logs showing vulnerability counts
   - `trivy-reports` artifact with JSON + table reports
   - CRITICAL/HIGH counts

3. **Nuclei Report (DAST)**
   - CI logs showing scan results against running container
   - `dast-reports` artifact with scan JSONs + summary
   - Missing headers and exposed panels findings

4. **Pipeline Evidence**
   - Green security phase in CI run
   - All 3 security tools running automatically on every PR

## Incident Response

If a security issue is found:

1. **Assess severity** - How critical is it?
2. **Create private issue** - Don't expose details publicly
3. **Fix in dedicated branch** - `security/fix-issue-name`
4. **Review by security-aware team member**
5. **Deploy fix immediately** after approval
6. **Post-mortem** - Document lessons learned
