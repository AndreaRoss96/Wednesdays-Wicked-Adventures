from app import db
from app.models import Role, Park

def seed_dev_data():
    # prevent duplicate seeding
    if Role.query.first() or Park.query.first():
        return

    # Roles
    admin_role = Role(name="admin")
    customer_role = Role(name="customer")

    db.session.add_all([admin_role, customer_role])
    db.session.commit()

    # Parks
    park1 = Park(
        name='PARK 1',
        location='Dublin',
        description='Dublin Park 1'
    )
    park2 = Park(
        name='PARK 2',
        location='London',
        description='London Park 2'
    )
    park3 = Park(
        name='PARK 3',
        location='Berlin',
        description='Belin Park 3'
    )

    db.session.add_all([park1, park2, park3])
    db.session.commit()
