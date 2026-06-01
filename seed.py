from app import create_app

from app.models import db

from app.models.role import Role
from app.models.user import User
from app.models.event_type import EventType

def seed_db(app):
    """Seed database with inital data."""
    
    with app.app_context():
        
        # creat clean database
        db.drop_all()
        db.create_all()
        
        # create roles
        administrator = Role.create(name="Administrator")
        organiser = Role.create(name="Organiser")
        coordinator = Role.create(name="Coordinator")
        attendee = Role.create(name="Attendee")
        
        # create user of each role
        User.create(email="admin@eventmaster.com",
                    password="admin",
                    full_name="Admin User",
                    role_id=administrator.id)
        
        User.create(email="organiser@eventmaster.com",
                    password="organiser",
                    full_name="Organiser User",
                    role_id=organiser.id)
        
        User.create(email="coordinator@eventmaster.com",
                    password="coordinator",
                    full_name="Coordinator User",
                    role_id=coordinator.id)
        
        User.create(email="attendee@eventmaster.com",
                    password="attendee",
                    full_name="Attendee User",
                    role_id=attendee.id)
        
        # create workshop event type
        EventType.create(name="Workshop")
        
        print("database seeded")
        
        
if __name__ == '__main__':
    app = create_app(config_filename='app.config.DevelopmentConfig')
    seed_db(app)