# Security

This document describes the security measures and tools used in the project.

## SAST - Static Application Security Testing

### Bandit

**Bandit** is a tool designed to find common security issues in Python code.

**Configuration:** `flask_app/.bandit.yml`

**Running locally:**
```bash
pip install bandit
bandit -r flask_app/src/main/app -c flask_app/.bandit.yml
```

**What Bandit checks:**

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

**CI Integration:**

Bandit runs in CI and blocks merges if HIGH severity issues are found.

### SAST Workflow

```yaml
- name: Run Bandit
  run: |
    pip install bandit
    bandit -r flask_app/src/main/app -f json -o bandit-report.json

- name: Upload Bandit Report
  uses: actions/upload-artifact@v4
  with:
    name: bandit-report
    path: bandit-report.json
```

## Application Security

### Password Security

Passwords are hashed using **PBKDF2-SHA256** (via Werkzeug):

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing password
hashed = generate_password_hash(password)

# Verifying password
is_valid = check_password_hash(stored_hash, provided_password)
```

**Never stored:**
- Plain text passwords
- Reversible encryption

### Authentication

**Flask-Login** manages user sessions:

- Session-based authentication
- `@login_required` decorator for protected routes
- Automatic session management

**Protected routes:**
- `/profile`
- `/bookings`
- `/booking/new`
- `/logout`

### CSRF Protection

**Cross-Site Request Forgery** protection:

| Environment | CSRF Status |
|-------------|-------------|
| Development | Disabled (for testing) |
| Production | **Enabled** |

Production config:
```python
WTF_CSRF_ENABLED = True
```

### Database Security

**Foreign Key Enforcement:**
```python
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
```

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

## Security Checklist

Before deploying to production:

- [ ] No hardcoded secrets in code
- [ ] Passwords properly hashed
- [ ] CSRF protection enabled
- [ ] Input validation on all forms
- [ ] SQL injection prevention (use ORM)
- [ ] XSS prevention (template escaping)
- [ ] Bandit scan passed
- [ ] Dependencies up to date

## Security Evidence for Assignment

To demonstrate security processes:

1. **Bandit Report**
   - Screenshot of scan results
   - Show no HIGH severity issues

2. **Security Workflow Run**
   - Green CI status
   - Artifact with security report

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
