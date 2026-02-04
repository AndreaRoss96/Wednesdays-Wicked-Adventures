# Wednesday's Wicked Adventures

**Horror Park Booking System**

## Project Overview

Wednesday's Wicked Adventures is a booking system for horror theme parks. The system allows customers to browse parks, create accounts, and book tickets for horror experiences.

### Key Features

- **User Registration & Authentication** - Secure account creation with password hashing
- **Park Browsing** - View available horror parks with descriptions and locations
- **Booking Management** - Create and view bookings for park visits
- **Admin Panel** - Flask-Admin integration for managing users, bookings, and parks
- **Contact Form** - Message system for customer inquiries

### User Roles

| Role | Permissions |
|------|-------------|
| **Customer** | Register, login, browse parks, create bookings, view own bookings |
| **Admin** | All customer permissions + Flask-Admin panel access |

### Available Parks

| Park | Location | Difficulty | Min Age |
|------|----------|------------|---------|
| Witches' Park | Dublin | Moderate | 10+ |
| Spider Park | London | Hard | 14+ |
| Haunted House | Berlin | Easy | 8+ |

## Tech Stack

- **Backend**: Python 3.11, Flask 3.1.2
- **Database**: SQLite (dev/test), configurable for production
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **Authentication**: Flask-Login
- **Admin**: Flask-Admin
- **Forms**: Flask-WTF, WTForms
- **CI/CD**: GitHub Actions
- **Quality**: SonarCloud, Flake8, Bandit (SAST)

## Quick Links

- [Local Setup Guide](setup-local.md)
- [CI/CD Pipeline](pipeline.md)
- [Testing & Quality](testing-quality.md)
- [Security](security.md)
- [Admin Guide](admin.md)

## Repository Structure

```
Wednesdays-Wicked-Adventures/
├── .github/
│   └── workflows/
│       └── pipeline.yaml      # CI/CD pipeline
├── flask_app/
│   └── src/
│       ├── main/
│       │   ├── app/           # Application code
│       │   │   ├── models.py  # Database models
│       │   │   ├── login.py   # Auth routes
│       │   │   ├── main.py    # Main routes
│       │   │   └── seed_data/ # Initial data
│       │   └── config.py      # Flask config
│       ├── tests/             # Test suites
│       ├── requirements.txt
│       └── Dockerfile
├── tests/                     # Smoke tests
├── docs/                      # Documentation (this site)
└── mkdocs.yml
```

## Team

**ATU DevOps Group 3**

For contribution guidelines, see [CONTRIBUTING.md](https://github.com/AndreaRoss96/Wednesdays-Wicked-Adventures/blob/main/CONTRIBUTING.md).
