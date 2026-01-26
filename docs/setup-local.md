# Local Development Setup

This guide explains how to set up and run the application locally.

## Prerequisites

- Python 3.9.7 or higher (CI uses Python 3.11)
- Git
- pip (Python package manager)

## Step 1: Clone the Repository

```bash
git clone https://github.com/L00188348/Wednesdays-Wicked-Adventures.git
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

| Package | Purpose |
|---------|---------|
| Flask | Web framework |
| flask-sqlalchemy | Database ORM |
| flask-login | User authentication |
| PyMySQL | MySQL database connector |
| werkzeug | Password hashing utilities |

## Step 4: Run the Application

```bash
export FLASK_APP=app:create_app
flask run
```

**Windows (PowerShell):**
```powershell
$env:FLASK_APP = "app:create_app"
flask run
```

The application will be available at: **http://localhost:5000**

## Database Setup

### Development Database

The development environment uses SQLite and automatically:

1. Creates the database file (`flask_app.db`)
2. Creates all tables
3. Seeds initial data (roles, parks)

No manual database setup is required for development.

### Database Shell Commands

Access the Flask shell for database operations:

```bash
export DEV_DATABASE_URL="sqlite:///flask_app.db"
export FLASK_APP=app:create_app
flask shell
```

In the shell:
```python
# Create all tables
db.create_all()

# Drop all tables
db.drop_all()

# Query data
from app.models import User, Park, Booking
User.query.all()
Park.query.all()
```

## Seed Data

The application automatically seeds the following data in development:

**Roles:**
- admin
- customer

**Parks:**
- PARK 1 (Dublin)
- PARK 2 (London)
- PARK 3 (Berlin)

## Environment Configuration

| Environment | Database | Debug | CSRF |
|-------------|----------|-------|------|
| Development | SQLite (local file) | Enabled | Disabled |
| Testing | TEST_DATABASE_URL env var | Disabled | - |
| Production | PROD_DATABASE_URL env var | Disabled | Enabled |

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
flask run --port 5001
```

**Module not found errors:**
Ensure you're in the correct directory (`flask_app/src/main`) and virtual environment is activated.

**Database errors:**
Delete `flask_app.db` and restart the application to recreate the database.
