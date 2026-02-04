# Admin Guide

This document covers administrative tasks and system management.

## Flask-Admin Panel

The project uses Flask-Admin for administrative operations.

**Access URL:** `http://localhost:5000/admin`

**Requirements:**
- Must be logged in
- Must have `admin` role

### Admin Views

| Model | Available Operations |
|-------|---------------------|
| Users | View, Create, Edit, Delete |
| Roles | View, Create, Edit, Delete |
| Parks | View, Create, Edit, Delete |
| Bookings | View, Create, Edit, Delete |
| Messages | View, Delete |

### User Management

**Columns displayed:**
- Name, Last Name, Email
- Password (hidden as `*****`)
- Role

**Features:**
- Search by name or email
- Filter by name or email
- Password is automatically hashed on save

### Booking Management

**Columns displayed:**
- Park, Date, Number of Tickets
- Health & Safety agreement
- User

**Features:**
- Search by park name or user name
- Filter by park or user

## User Roles

### Role Permissions

| Role | Create Booking | View Own Bookings | Admin Panel Access |
|------|----------------|-------------------|-------------------|
| Customer | Yes | Yes | No |
| Admin | Yes | Yes | **Yes** |

### Admin Credentials

Default admin users (seeded):
- `admin1@example.com`
- `admin2@example.com`

Password is set via `SEED_ADMIN_PASSWORD` environment variable.

## Database Management

### Accessing Flask Shell

```bash
cd flask_app/src/main
export FLASK_APP=app
flask shell
```

### Common Database Operations

**View all users:**
```python
from app.models import User
User.query.all()
```

**Find user by email:**
```python
User.query.filter_by(email='user@example.com').first()
```

**View all bookings:**
```python
from app.models import Booking
Booking.query.all()
```

**View all parks:**
```python
from app.models import Park
Park.query.all()
```

### Modifying Data

**Update booking:**
```python
from app import db
booking = db.session.get(Booking, booking_id)
booking.num_tickets = 5
db.session.commit()
```

**Delete booking:**
```python
booking = db.session.get(Booking, booking_id)
db.session.delete(booking)
db.session.commit()
```

**Create new admin user:**
```python
from app.models import User, Role
from werkzeug.security import generate_password_hash
from app import db

admin_role = Role.query.filter_by(name='admin').first()
admin = User(
    name='New',
    last_name='Admin',
    email='newadmin@example.com',
    password=generate_password_hash('secure_password', method='pbkdf2:sha256'),
    role=admin_role
)
db.session.add(admin)
db.session.commit()
```

## Database Schema

### Entity Relationship

```
┌─────────┐       ┌─────────┐
│  Role   │◄──────│  User   │
└─────────┘       └────┬────┘
                       │
                      \│/
┌─────────┐       ┌─────────┐
│  Park   │◄──────│ Booking │
└─────────┘       └─────────┘

┌─────────┐
│ Message │ (standalone)
└─────────┘
```

### Tables

**users**

| Column | Type | Constraints |
|--------|------|-------------|
| user_id | Integer | Primary Key |
| name | String(100) | Not Null |
| last_name | String(100) | Not Null |
| email | String(100) | Unique |
| password | String(100) | Not Null |
| role_id | Integer | Foreign Key (roles) |

**roles**

| Column | Type | Constraints |
|--------|------|-------------|
| role_id | Integer | Primary Key |
| name | String(64) | Unique |

**parks**

| Column | Type | Constraints |
|--------|------|-------------|
| park_id | Integer | Primary Key |
| name | String(150) | Not Null |
| location | String(150) | Not Null |
| description | String(100) | Not Null |
| image_path | String(200) | Default value |
| short_description | String(80) | Not Null |
| slug | String(100) | Unique, Not Null |
| folder | String(50) | Default empty |
| hours | String(100) | Default value |
| difficulty | String(50) | Default 'Moderate' |
| min_age | Integer | Default 12 |
| price | String(50) | Default value |
| wait_time | String(50) | Default value |
| height_requirement | String(50) | Default value |

**bookings**

| Column | Type | Constraints |
|--------|------|-------------|
| booking_id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users), Not Null |
| park_id | Integer | Foreign Key (parks), Not Null |
| date | DateTime | Not Null |
| num_tickets | Integer | Not Null, Default 1 |
| health_safety | Boolean | Not Null, Default False |

**messages**

| Column | Type | Constraints |
|--------|------|-------------|
| message_id | Integer | Primary Key |
| name | String(100) | Not Null |
| email | String(100) | Not Null |
| message | Text | Not Null |
| created_at | DateTime | Default now() |

## Environment Configuration

### Configuration Classes

| Class | Usage | Database |
|-------|-------|----------|
| DevelopmentConfig | Local dev | SQLite (auto-created) |
| TestingConfig | CI/Tests | SQLite in-memory |
| ProductionConfig | Production | From `PROD_DATABASE_URL` |

### Environment Variables

**Development:**
```bash
export SECRET_KEY="dev-secret-key"
export SEED_ADMIN_PASSWORD="admin-password"
export FLASK_APP=app
```

**Production:**
```bash
export PROD_DATABASE_URL="mysql+pymysql://user:pass@host/db"
export SECRET_KEY="production-secret-key"
export FLASK_ENV=production
```

## Backup & Recovery

### Database Backup (SQLite)

```bash
# Backup
cp flask_app.db flask_app_backup_$(date +%Y%m%d).db

# Restore
cp flask_app_backup_20240115.db flask_app.db
```

### Database Reset

```bash
# Delete database (in flask_app/src/main)
rm flask_app.db

# Restart app (auto-recreates with seed data)
flask --app app run
```

## Troubleshooting

### Common Issues

**"No such table" error:**
```python
# In flask shell
from app import db
db.create_all()
```

**"IntegrityError" on insert:**
- Check foreign key constraints
- Ensure referenced records exist

**Login not working:**
- Verify password hashing
- Check user exists in database
- Verify role_id is valid

**Admin panel access denied:**
- Ensure user has `admin` role
- Check `has_role('admin')` returns True

**500 Internal Server Error:**
- Check Flask logs
- Enable debug mode
- Verify database connection
- Check SECRET_KEY is set
