# Wednesday's Wicked Adventures

Repo for DevOps Project Management Assignment Group 3

**Horror Park Booking System** - A booking platform for horror theme parks.

## Contributing

1. Create feature branch: `git checkout -b feature/SCRUM-XX-description`
2. Make changes and commit
3. Create PR to `main` branch
4. CI pipeline runs automatically
5. After approval, merge to `main`

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

Full project documentation is available in the [docs/](docs/) folder and is automatically built on every PR.

- [Project Overview](docs/index.md)
- [Local Setup Guide](docs/setup-local.md)
- [CI/CD Pipeline](docs/pipeline.md)
- [Testing & Quality](docs/testing-quality.md)
- [Security](docs/security.md)
- [Admin Guide](docs/admin.md)

## Quick Start

```bash
cd flask_app/src/main
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# Set required environment variables
export SECRET_KEY="your-secret-key"
export SEED_ADMIN_PASSWORD="your-admin-password"

flask --app app run
```

## Tech Stack

- Python 3.11
- Flask 3.1.2
- SQLAlchemy + Flask-SQLAlchemy
- Flask-Login
- Flask-Admin
- SQLite (dev) / MySQL (configurable)

## Testing Packages

- pytest 7.4.3
- pytest-cov 4.1.0
- pytest-flask 1.3.0
- coverage 7.3.2
