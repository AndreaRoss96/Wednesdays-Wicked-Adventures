# Local Development Setup

This guide explains how to set up and run the application locally.

## Prerequisites

- Python 3.9.7 or higher (CI uses Python 3.11)
- Git
- pip (Python package manager)

## Step 1: Clone the Repository

```bash
git clone https://github.com/AndreaRoss96/Wednesdays-Wicked-Adventures.git
cd Wednesdays-Wicked-Adventures
```

## Step 2: Create Virtual Environment

```bash
cd flask_app/src/main
python -m venv venv
```

Activate the virtual environment:

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r ../requirements.txt
```

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.1.2 | Web framework |
| flask-sqlalchemy | 3.1.1 | Database ORM |
| flask-login | 0.6.3 | User authentication |
| Flask-Admin | 1.6.1 | Admin panel |
| Flask-WTF | 1.2.2 | Form handling with CSRF |
| python-dotenv | 1.2.1 | Environment variables |
| flake8 | 7.3.0 | Code linting |

### Testing Packages

| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4.3 | Test framework |
| pytest-cov | 4.1.0 | Coverage reporting |
| pytest-flask | 1.3.0 | Flask test utilities |

## Step 4: Environment Variables

Create a `.env` file in `flask_app/src/` directory:

```bash
SECRET_KEY=your-secret-key-here
SEED_ADMIN_PASSWORD=your-admin-password
```

**Important:** `SEED_ADMIN_PASSWORD` is required for database seeding.

## Step 5: Run the Application

```bash
cd flask_app/src/main
flask --app app run
```

The application will be available at: **http://localhost:5000**

## Database Setup

### Development Database

The development environment uses SQLite and automatically:

1. Creates the database file (`flask_app.db`)
2. Creates all tables
3. Seeds initial data (roles, parks, admin users)

No manual database setup is required for development.

### Seeded Data

**Roles:**

- admin
- customer

**Parks:**

- Witches' Park (Dublin) - Moderate difficulty, 10+
- Spider Park (London) - Hard difficulty, 14+
- Haunted House (Berlin) - Easy difficulty, 8+

**Admin Users:**

- admin1@example.com
- admin2@example.com

(Password from SEED_ADMIN_PASSWORD environment variable)

## Environment Configuration

| Environment | Database | Debug | CSRF |
|-------------|----------|-------|------|
| Development | SQLite (local file) | Enabled | Enabled |
| Testing | SQLite in-memory | Disabled | Disabled |
| Production | PROD_DATABASE_URL env var | Disabled | Enabled |

## Running with Docker

```bash
cd flask_app/src
docker build -t wicked-adventures .
docker run -p 5000:5000 -e SECRET_KEY=xxx -e SEED_ADMIN_PASSWORD=xxx wicked-adventures
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
flask --app app run --port 5001
```

**Module not found errors:**
Ensure you're in the correct directory (`flask_app/src/main`) and virtual environment is activated.

**SEED_ADMIN_PASSWORD not set:**
The application requires this environment variable for database seeding. Set it in `.env` file or export it.

**Database errors:**
Delete `flask_app.db` and restart the application to recreate the database.
