# Wednesday's Wicked Adventures

**Horror Park Booking System**

## Project Overview

Wednesday's Wicked Adventures is a booking system for horror theme parks. The system allows customers to browse parks, create accounts, and book tickets for horror experiences.

### Key Features

- **User Registration & Authentication** - Secure account creation with password hashing
- **Park Browsing** - View available horror parks with descriptions and locations
- **Booking Management** - Create and view bookings for park visits
- **Admin Management** - Administrative users can manage bookings and park data

### User Roles

| Role | Permissions |
|------|-------------|
| **Customer** | Register, login, browse parks, create bookings, view own bookings |
| **Admin** | All customer permissions + manage all bookings and users |

### Business Rule

> Customers cannot edit their booking details after submission. Only administrators have the ability to modify booking information.

## Tech Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite (dev), MySQL (prod)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **CI/CD**: GitHub Actions
- **Quality**: SonarCloud, Bandit (SAST)

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
│   ├── workflows/          # CI/CD pipelines
│   └── pull_request_template.md
├── flask_app/
│   └── src/
│       ├── requirements.txt
│       └── main/
│           ├── config.py   # Flask configuration
│           └── app/        # Application code
├── tests/                  # Test suites
├── docs/                   # Documentation (this site)
└── mkdocs.yml
```

## Team

**ATU DevOps Group 3**

For contribution guidelines, see [CONTRIBUTING.md](https://github.com/L00188348/Wednesdays-Wicked-Adventures/blob/main/CONTRIBUTING.md).
