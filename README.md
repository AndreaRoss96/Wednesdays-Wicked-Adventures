# Wednesday's Wicked Adventures

Repo for DevOps Project Management Assignment Group 3

**Horror Park Booking System** - A booking platform for horror theme parks.

## Quick Start

```bash
cd flask_app/src/main
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt
flask --app app run
```

## Contributing

1. Create feature branch: `git checkout -b feature/SCRUM-XX-description`
2. Make changes and commit
3. Create PR to `main` branch
4. Minimum 1 approval required before merge

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Documentation

Full project documentation is available in the [docs/](docs/) folder and is automatically built on every PR.

- [Project Overview](docs/index.md)
- [Local Setup Guide](docs/setup-local.md)
- [CI/CD Pipeline](docs/pipeline.md)
- [Testing & Quality](docs/testing-quality.md)
- [Security](docs/security.md)
- [Admin Guide](docs/admin.md)

## Tech Stack

- Python 3.9.7+
- Flask==3.1.2
- flask-sqlalchemy==3.1.1
- SQLAlchemy-Utils==0.42.1
- PyMySQL==1.1.2
- flask-login==0.6.3
- Flask-Admin==1.6.1
- WTForms==3.1.2

## Testing packages

- pytest==7.4.3
- pytest-cov==4.1.0
- pytest-flask==1.3.0
- coverage==7.3.2