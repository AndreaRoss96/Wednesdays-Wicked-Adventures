# Admin Guide

This document covers administrative tasks and system management.

## User Roles

### Role Permissions

| Role | Create Booking | View Own Bookings | Edit Any Booking | Manage Users |
|------|----------------|-------------------|------------------|--------------|
| Customer | Yes | Yes | No | No |
| Admin | Yes | Yes | **Yes** | **Yes** |

### Business Rule

> Customers cannot edit their booking details after submission. Only administrators have the ability to modify booking information.

## Database Management

### Accessing Database Shell

```bash
cd flask_app/src/main
export FLASK_APP=app:create_app
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

**View bookings for specific user:**
```python
user = User.query.get(1)
user.bookings
```

**View all parks:**
```python
from app.models import Park
Park.query.all()
```

### Modifying Data

**Update booking:**
```python
booking = Booking.query.get(booking_id)
booking.num_tickets = 5
db.session.commit()
```

**Delete booking:**
```python
booking = Booking.query.get(booking_id)
db.session.delete(booking)
db.session.commit()
```

**Create admin user:**
```python
from app.models import User, Role
from werkzeug.security import generate_password_hash

admin_role = Role.query.filter_by(name='admin').first()
admin = User(
    name='Admin',
    last_name='User',
    email='admin@example.com',
    password=generate_password_hash('secure_password'),
    role_id=admin_role.role_id
)
db.session.add(admin)
db.session.commit()
```

## Database Schema

### Entity Relationship

```
┌─────────┐       ┌─────────┐
│  Role   │──────<│  User   │
└─────────┘       └─────────┘
                       │
                       │
                      \│/
┌─────────┐       ┌─────────┐
│  Park   │──────<│ Booking │
└─────────┘       └─────────┘
```

### Tables

**users**
| Column | Type | Constraints |
|--------|------|-------------|
| user_id | Integer | Primary Key |
| name | String(100) | Not Null |
| last_name | String(100) | Not Null |
| email | String(100) | Unique, Not Null |
| password | String(200) | Not Null |
| role_id | Integer | Foreign Key (roles) |

**roles**
| Column | Type | Constraints |
|--------|------|-------------|
| role_id | Integer | Primary Key |
| name | String(50) | Not Null |

**parks**
| Column | Type | Constraints |
|--------|------|-------------|
| park_id | Integer | Primary Key |
| name | String(100) | Not Null |
| location | String(100) | |
| description | String(500) | |

**bookings**
| Column | Type | Constraints |
|--------|------|-------------|
| booking_id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users) |
| park_id | Integer | Foreign Key (parks) |
| date | Date | Not Null |
| num_tickets | Integer | Not Null |
| health_safety | Boolean | Default: False |

## Environment Configuration

### Configuration Classes

| Class | Usage | Database |
|-------|-------|----------|
| DevelopmentConfig | Local dev | SQLite (auto-created) |
| TestingConfig | CI/Tests | From `TEST_DATABASE_URL` |
| ProductionConfig | Production | From `PROD_DATABASE_URL` |

### Environment Variables

**Development:**
```bash
export DEV_DATABASE_URL="sqlite:///flask_app.db"
export FLASK_APP=app:create_app
```

**Production:**
```bash
export PROD_DATABASE_URL="mysql+pymysql://user:pass@host/db"
export FLASK_ENV=production
```

## Monitoring & Logs

### Flask Debug Mode

Development mode includes:
- Detailed error pages
- Auto-reload on code changes
- Debug toolbar (if installed)

### Logging

Add logging to application:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("User logged in: %s", user.email)
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
# Delete database
rm flask_app.db

# Restart app (auto-recreates with seed data)
flask run
```

## Troubleshooting

### Common Issues

**"No such table" error:**
```python
# In flask shell
db.create_all()
```

**"IntegrityError" on insert:**
- Check foreign key constraints
- Ensure referenced records exist

**Login not working:**
- Verify password hashing
- Check user exists in database
- Verify role_id is valid

**500 Internal Server Error:**
- Check Flask logs
- Enable debug mode
- Verify database connection
