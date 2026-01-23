from app import db
from app.models import User, Role, Park
from werkzeug.security import generate_password_hash
import os

def seed_dev_data():
    # prevent duplicate seeding
    if Role.query.first() or Park.query.first():
        return

    # Roles
    admin_role = Role(name="admin")
    customer_role = Role(name="customer")

    db.session.add_all([admin_role, customer_role])
    db.session.commit()

    # Retrieve password from environment or use a secure fallback for local dev only
    # !!! For production, ensure the env var is set and remove the default value. !!!
    dev_password = os.environ.get("SEED_ADMIN_PASSWORD")
    
    if not dev_password:
        raise ValueError("SEED_ADMIN_PASSWORD environment variable is not set.")

    # Admin users
    admin1 = User(
        name="Admin",
        last_name="One",
        email="admin1@example.com",
        password=generate_password_hash(dev_password, method='pbkdf2:sha256'),
        role=admin_role
    )

    admin2 = User(
        name="Admin",
        last_name="Two",
        email="admin2@example.com",
        password=generate_password_hash(dev_password, method='pbkdf2:sha256'),
        role=admin_role
    )

    db.session.add_all([admin1, admin2])
    db.session.commit()

    # Parks
    park1 = Park(
        name='Witches\' Park',
        location='Dublin',
        description="""
        Welcome to the Witches' Park, where magic comes alive! 
        Experience spell-binding attractions, potion-making workshops, 
        and encounter mystical creatures in our enchanted forest.
        
        • Spell Casting Arena - Test your magical abilities
        • Potion Brewing Lab - Create your own magical elixirs
        • Witch Training Academy - Learn spells from master witches
        • Enchanted Forest Walk - Discover hidden magical creatures
        """,
        short_description='Step into a world of spells. Feel the magic all around you.',
        slug='park-1-dublin',
        image_path='images/parks/witches/hat.png',
        folder='witches',
        hours='10:00 AM - 8:00 PM',
        difficulty='Moderate',
        min_age=10,
        price='Starting at $39.99',
        wait_time='20-40 minutes',
        height_requirement='42" (1.07m)',
    )
    park2 = Park(
        name='Spider Park',
        location='London',
        description="""
        Dare to enter our arachnid-infested domain! Navigate through giant webs, 
        face enormous spiders, and experience the ultimate thrill in darkness.
        
        • Giant Web Maze - Navigate through intricate spider webs
        • Spider Cavern - Face giant arachnids in their natural habitat
        • Arachnid Alley - Walk through a corridor of crawling spiders
        • Venom Drop Ride - Free fall through a spider-infested shaft
        """,
        short_description='Enter the web of fear and thrill. Face the spiders if you dare.',
        slug='park-2-london',
        image_path='images/parks/spider/spider.png',
        folder='spider',
        hours='9:00 AM - 10:00 PM',
        difficulty='Hard',
        min_age=14,
        price='Starting at $54.99',
        wait_time='45-75 minutes',
        height_requirement='54" (1.37m)',
    )
    park3 = Park(
        name='Haunted House',
        location='Berlin',
        description="""
        The ancient manor holds dark secrets. Wander through haunted halls, 
        encounter restless spirits, and uncover mysteries that chill to the bone.
        
        • Ghostly Galleries - Walk through portraits that come alive
        • Crypt of Whispers - Hear the secrets of the departed
        • Hall of Echoes - Where every step resonates with past tragedies
        • Séance Room - Experience a simulated supernatural encounter
        """,
        short_description='Walk among the restless dead. Discover the shadows that await.',
        slug='park-3-berlin',
        image_path='images/parks/haunted/skull.png',
        folder='haunted',
        hours='6:00 PM - 2:00 AM',
        difficulty='Easy',
        min_age=8,
        price='Starting at $29.99',
        wait_time='15-30 minutes',
        height_requirement='None',
    )

    db.session.add_all([park1, park2, park3])
    db.session.commit()
