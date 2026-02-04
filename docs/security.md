# Security

This document describes the security measures and tools used in the project.

## SAST - Static Application Security Testing

### Bandit

**Bandit** is a tool designed to find common security issues in Python code.

**Running locally:**
```bash
cd flask_app/src/main
pip install bandit
bandit -r . -f json -o bandit-results.json
```

**CI Integration:**

Bandit runs automatically in the CI pipeline (Phase 5):
```yaml
- name: Security Scan (SAST)
  run: |
    pip install bandit
    bandit -r . -f json -o bandit-results.json
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

**Configuration:**
```python
# config.py
class DevelopmentConfig(Config):
    WTF_CSRF_ENABLED = True

class TestingConfig(Config):
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    WTF_CSRF_ENABLED = True
```

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
- [ ] Bandit scan passed
- [ ] Dependencies up to date

## DAST - Dynamic Application Security Testing

### Planned Implementation

DAST scans the running application for vulnerabilities:

**Tool:** OWASP ZAP (Zed Attack Proxy)

**Scan Types:**
- Baseline scan (quick)
- Full scan (comprehensive)

**Integration Plan:**
1. Deploy app to test environment
2. Run ZAP baseline scan
3. Generate report
4. Fail pipeline on high-severity findings

## Security Evidence for Assignment

To demonstrate security processes:

1. **Bandit Report**
   - Screenshot of scan results in CI logs
   - Show severity breakdown

2. **CI Security Phase**
   - Green status on security step
   - bandit-results.json artifact

3. **Code Review**
   - Security-focused review comments
   - Evidence of security fixes

## Incident Response

If a security issue is found:

1. **Assess severity** - How critical is it?
2. **Create private issue** - Don't expose details publicly
3. **Fix in dedicated branch** - `security/fix-issue-name`
4. **Review by security-aware team member**
5. **Deploy fix immediately** after approval
6. **Post-mortem** - Document lessons learned
