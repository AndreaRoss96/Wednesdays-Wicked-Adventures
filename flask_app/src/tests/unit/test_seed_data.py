from datetime import datetime
from app import create_app, db
from app.models import Role, User, Park, Booking

def seed_test_data():
    app = create_app(testing=True)

    with app.app_context():
        # 🔥 Clean slate — avoids FK constraint errors
        db.drop_all()
        db.create_all()

        # ---------- Roles ----------
        admin_role = Role(name="admin")
        user_role = Role(name="user")

        db.session.add_all([admin_role, user_role])
        db.session.commit()

        # ---------- Users ----------
        admin_user = User(
            name="Admin",
            last_name="User",
            email="admin@test.com",
            password="hashedpassword",
            role=admin_role
        )

        normal_user = User(
            name="John",
            last_name="Doe",
            email="user@test.com",
            password="hashedpassword",
            role=user_role
        )

        db.session.add_all([admin_user, normal_user])
        db.session.commit()

        # ---------- Parks ----------
        park = Park(
            name="Adventure Park",
            location="Wonderland",
            description="A fun adventure park",
            short_description="Fun park",
            slug="adventure-park",
            folder="adventure"
        )

        db.session.add(park)
        db.session.commit()

        # ---------- Bookings ----------
        booking = Booking(
            user_id=normal_user.user_id,
            park_id=park.park_id,
            date=datetime.utcnow(),
            num_tickets=2,
            health_safety=True
        )

        db.session.add(booking)
        db.session.commit()

        print("✅ Test database seeded successfully.")

if __name__ == "__main__":
    seed_test_data()
