from app import create_app
from app.extensions import db

def reset_db():
    app = create_app('development')
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating tables...")
        db.create_all()
        print("Database reset complete!")

if __name__ == "__main__":
    reset_db()