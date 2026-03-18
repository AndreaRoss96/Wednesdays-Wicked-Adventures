# Wednesday's Wicked Adventures

A booking platform for horror theme parks. Built as a DevOps project management assignment by Group 3 at ATU Galway.

The idea is simple: users pick a park, pick a date, and book tickets. Behind the scenes there is a full CI/CD pipeline, three layers of security scanning, automated tests, and a Docker container that gets vulnerability-checked on every push.

---

## The Parks

Three parks are seeded into the database by default:

| Park | Location | Difficulty | Min Age | Price from |
|------|----------|------------|---------|------------|
| Witches' Park | Dublin | Moderate | 10 | $39.99 |
| Spider Park | London | Hard | 14 | $54.99 |
| Haunted House | Berlin | Easy | 8 | $29.99 |

---

## Tech Stack

| Category | What we use |
|----------|-------------|
| Language | Python 3.11 |
| Web framework | Flask 3.1.2 |
| ORM | SQLAlchemy via flask-sqlalchemy |
| Auth | Flask-Login |
| Admin panel | Flask-Admin 1.6.1 |
| Forms + CSRF | WTForms 3.1.2, Flask-WTF |
| Database | SQLite (dev/test), MySQL (production) |
| Testing | pytest 7.4.3, pytest-cov, pytest-flask |
| SAST | Bandit |
| Container scan | Trivy |
| DAST | Nuclei |
| Code quality | Flake8, SonarCloud |
| CI/CD | GitHub Actions |
| Containerisation | Docker (python:3.9-slim) |
| Docs | MkDocs Material theme |

---

## Quick Start

```bash
git clone https://github.com/AndreaRoss96/Wednesdays-Wicked-Adventures.git
cd Wednesdays-Wicked-Adventures/flask_app/src/main

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r ../requirements.txt

export SECRET_KEY="any-local-key"
export SEED_ADMIN_PASSWORD="xxxxxx" # by reqest

flask --app app run
```

App runs at `http://127.0.0.1:5000`.

The database is created and seeded automatically on first run. Default admin login is `admin@example.com` with whatever password you set in `SEED_ADMIN_PASSWORD`.

### Run with Docker

```bash
cd flask_app/src

docker build -t wicked-adventures .

docker run -p 5000:5000 \
  -e SECRET_KEY="local-key" \
  -e SEED_ADMIN_PASSWORD="xxxxxx" \  # by reqest
  wicked-adventures
```

---

## Project Structure

```
Wednesdays-Wicked-Adventures/
|
+-- .github/
|   +-- workflows/
|   |   +-- pipeline.yaml          # main CI/CD pipeline
|   +-- pull_request_template.md
|
+-- flask_app/
|   +-- src/
|       +-- main/
|       |   +-- app/
|       |       +-- __init__.py    # app factory
|       |       +-- main.py        # main routes
|       |       +-- login.py       # auth routes
|       |       +-- models.py      # db models + admin views
|       |       +-- config.py      # dev / test / prod configs
|       |       +-- seed_data/     # default parks, users, roles
|       |       +-- templates/     # Jinja2 HTML templates
|       |       +-- static/        # css, js, images
|       +-- tests/
|       |   +-- unit/              # model + auth tests
|       |   +-- integration/       # route + flow tests
|       |   +-- smoke/             # startup checks
|       |   +-- conftest.py        # fixtures
|       +-- Dockerfile
|       +-- requirements.txt
|       +-- pytest.ini
|       +-- setup.py
|       +-- sonar-project.properties
|
+-- docs/                          # MkDocs source files
+-- mkdocs.yml
+-- CONTRIBUTING.md
+-- SOCIAL_CONTRACT.md
+-- README.md
```

---

## Running Tests

```bash
cd flask_app/src

# run everything
python -m pytest

# with coverage report
python -m pytest --cov=app --cov-report=html --cov-report=term-missing

# specific suite
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/smoke/
```

Test results and HTML coverage report go to `htmlcov/`.

### Test layout

- **unit/** - password hashing, model CRUD, seed data verification
- **integration/** - login, register, logout, booking flow, contact form, 404 handling
- **smoke/** - checks the app starts and basic public routes return 200

Fixtures in `conftest.py` spin up an in-memory SQLite database per test session with pre-seeded roles, one test user (`test@example.com / password123`), and three parks.

---

## CI/CD Pipeline

Every push to a feature branch and every PR to main runs the full pipeline. There are three jobs.

### Job 1: CI Pipeline

| Phase | What happens |
|-------|-------------|
| Setup | Python 3.11 venv, install dependencies |
| Flake8 | Critical errors block the build; style warnings are reported |
| Bandit | SAST scan of `flask_app/src/main/app`, results saved as artifact |
| Smoke tests | Quick check that the app starts correctly |
| Full tests | Complete pytest run with coverage XML for SonarCloud |
| SonarCloud | Static analysis upload, quality gate check |
| Summary | Phase-by-phase build report |

### Job 2: Docker Build, Test and Push (runs after Job 1)

| Phase | What happens |
|-------|-------------|
| Build | Builds `wicked-adventures:latest` from `flask_app/src/Dockerfile` |
| Trivy | Container vulnerability scan, HIGH/CRITICAL severity filter, saves report as artifact |
| Container test | Starts container on port 5000, checks HTTP response and resource usage |
| Nuclei DAST | Three scans: critical CVEs, missing security headers, exposed admin panels |
| Push to Docker Hub | Tags and pushes the tested image with two tags: `latest` and the full commit SHA |
| Summary | Build and scan report |

The commit SHA tag gives a traceable history of every pushed image. If something breaks in production, the exact image version can be identified and rolled back.

### Job 3: Deploy to EC2 (runs after Job 2)

Deploys the tested Docker image to an AWS EC2 instance via SSH.

What it does on the remote server:
- Logs in to Docker Hub and pulls the latest image
- Generates a container name based on the first 12 characters of the image digest (e.g. `wicked-adventures-a3f9c12d4b71`)
- Stops and removes all previous `wicked-adventures-*` containers
- Starts the new container on port 80 with production environment variables

The container naming scheme based on image digest means each deployment has a unique, traceable name that ties back to the exact image that was built and tested in the pipeline.

Required secrets for this job: `EC2_SSH_KEY`, `EC2_HOST`, `EC2_USER`.

Note: the deploy stage requires the EC2 instance to be running. If the server is stopped, this job will fail at the SSH connection step. The CI and Docker jobs are not affected.

### Job 4: Build Documentation (runs in parallel with everything else)

Validates docs structure and runs `mkdocs build --strict`. The built site is saved as a `docs-site` artifact.

---

## Security

Password hashing uses PBKDF2-SHA256 via Werkzeug. CSRF protection is on by default through Flask-WTF. Sessions are managed by Flask-Login.

The pipeline runs three scanning tools:

**Bandit** scans Python source code for common security issues. It runs in Phase 5 of Job 1 and uploads results to the `security-reports` artifact.

**Trivy** scans the Docker image for known CVEs. It reports HIGH and CRITICAL severity findings. Results go to the `trivy-reports` artifact.

**Nuclei** runs dynamic scans against a live container. It checks for critical vulnerabilities, missing HTTP security headers, and exposed admin or debug endpoints. Results go to `dast-reports`.

Admin panel access is restricted to users with the `admin` role. All admin views inherit from a base class that checks role before rendering.

---

## Database Schema

```
users
  user_id       INTEGER  PK
  name          VARCHAR(100)
  last_name     VARCHAR(100)
  email         VARCHAR(100)  UNIQUE
  password      VARCHAR(255)  (hashed)
  role_id       FK -> roles.role_id

roles
  role_id       INTEGER  PK
  name          VARCHAR(64)   UNIQUE

parks
  park_id       INTEGER  PK
  name          VARCHAR(150)
  location      VARCHAR(150)
  description   VARCHAR(100)
  image_path    VARCHAR(200)
  slug          VARCHAR(100)  UNIQUE
  hours         VARCHAR(100)
  difficulty    VARCHAR(50)
  min_age       INTEGER
  price         VARCHAR(50)
  wait_time     VARCHAR(50)
  height_requirement  VARCHAR(50)

bookings
  booking_id    INTEGER  PK
  user_id       FK -> users.user_id
  park_id       FK -> parks.park_id
  date          DATETIME
  num_tickets   INTEGER
  health_safety BOOLEAN

messages
  message_id    INTEGER  PK
  name          VARCHAR(100)
  email         VARCHAR(100)
  message       TEXT
  created_at    DATETIME
```

---

## Application Routes

| Method | Route | Description | Auth required |
|--------|-------|-------------|---------------|
| GET | / | Homepage with park listing | No |
| GET | /parks/\<park_id\> | Park detail page | No |
| GET, POST | /login | Login form | No |
| GET, POST | /register | Registration form | No |
| GET, POST | /forgot_password | Password reset | No |
| GET | /logout | Logout | Yes |
| GET | /profile | User profile and bookings | Yes |
| GET, POST | /booking/new | Create new booking | Yes |
| POST | /contact | Submit contact form | No |
| GET | /health-safety-guidelines | Safety guidelines | Yes |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| SECRET_KEY | Yes | Flask session encryption key |
| SEED_ADMIN_PASSWORD | Dev/CI | Password for the seeded admin account |
| PROD_DATABASE_URL | Production | Full database connection string |
| DEV_DATABASE_URL | Optional | Overrides default SQLite path |
| FLASK_ENV | Optional | Environment name |

## GitHub Actions Secrets

The pipeline uses the following secrets configured in the repository settings:

| Secret | Used in | Description |
|--------|---------|-------------|
| SECRET_KEY | All jobs | Flask secret key passed to the app |
| SEED_ADMIN_PASSWORD | CI, Docker | Admin password for seeded data |
| SONAR_TOKEN | Job 1 | Authentication for SonarCloud analysis |
| GITHUB_TOKEN | Job 1 | Provided automatically by GitHub Actions |
| DOCKER_HUB_USERNAME | Job 2 | Docker Hub account name |
| DOCKER_HUB_ACCESS_TOKEN | Job 2 | Docker Hub access token for push |
| EC2_SSH_KEY | Job 3 | Private SSH key for the EC2 instance |
| EC2_HOST | Job 3 | Public IP or hostname of the EC2 server |
| EC2_USER | Job 3 | SSH user on the EC2 instance |

---

## Documentation

Full documentation lives in the `docs/` folder and is built automatically on every PR.

- [Project Overview](docs/index.md)
- [Local Setup Guide](docs/setup-local.md)
- [CI/CD Pipeline](docs/pipeline.md)
- [Testing and Quality](docs/testing-quality.md)
- [Security](docs/security.md)
- [Admin Guide](docs/admin.md)

---

## Contributing

1. Create a branch: `git checkout -b feature/SCRUM-XX-short-description`
2. Make changes, write tests if applicable
3. Run tests locally before opening a PR
4. Open a PR to `main`
5. Wait for CI to pass and at least one approval
6. Merge

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details. The team working agreements are in [SOCIAL_CONTRACT.md](SOCIAL_CONTRACT.md).

---

## Team

Group 3, ATU Galway, DevOps Project Management module.

- Andrea Rossolini
- Jesus Acuna
- Renata Ribeiro
- Romulo Barbosa
- Serhii Spitsyn
